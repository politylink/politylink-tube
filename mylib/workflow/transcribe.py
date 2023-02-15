import os
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import List

import pandas as pd

from mylib.audio.models import AudioModel
from mylib.audio.vad import VoiceActivityDetector
from mylib.workflow.models import BaseOperator, BashOperator, PythonOperator, StatusCode

LOGGER = getLogger(__name__)


@dataclass
class TranscribeRequest:
    m3u8_url: str
    out_dir: [Path | str]
    datetime: datetime


class TranscribeJobScheduler:
    def __init__(self):
        self.failed_jobs = []

    def schedule_batch(self, requests: List[TranscribeRequest]) -> List[BaseOperator]:
        jobs = []
        requests = sorted(requests, key=lambda x: x.datetime, reverse=True)  # prioritize the latest when tie-break
        for job_input in requests:
            jobs += self.schedule(job_input)
        jobs = sorted(jobs, key=lambda x: x.context.priority, reverse=True)
        return jobs

    def schedule(self, request: TranscribeRequest) -> List[BaseOperator]:
        out_dir = Path(request.out_dir)
        data_dir = out_dir / 'data'
        log_dir = out_dir / 'log'
        mp3_fp = data_dir / 'audio.mp3'
        vad_fp = data_dir / 'vad.csv'
        transcript_fp = data_dir / 'transcript.csv'

        jobs = [
            InitDirJob(out_dir),
            AudioDownloadJob(request.m3u8_url, mp3_fp),
            VADJob(mp3_fp, vad_fp)
        ]

        if vad_fp.exists():
            vad_df = pd.read_csv(vad_fp)

            # generate wav files
            wav_fps = []
            for _, row in vad_df.iterrows():
                wav_fp = data_dir / '{}.wav'.format(row['id'])
                wav_fps.append(wav_fp)
                jobs.append(AudioSplitJob(audio_fp=mp3_fp, start_sec=row['start_sec'],
                                          end_sec=row['end_sec'], out_fp=wav_fp))

            # transcribe by whisper
            result_fps = []
            for wav_fp in wav_fps:
                log_fp = log_dir / 'whisper_{}.log'.format(wav_fp.stem)
                result_fps.append(WhisperJob.get_result_fp(wav_fp))
                jobs.append(WhisperJob(wav_fp, log_fp))

            # summarize
            jobs.append(MergeWhisperJob(vad_fp=vad_fp, result_fps=result_fps, out_fp=transcript_fp))

        jobs = list(filter(self.filter_job, jobs))
        return jobs

    def filter_job(self, job):
        if job in self.failed_jobs:
            return False
        if job.pre_execute() != StatusCode.SUCCESS:
            return False
        return True

    def record_failed_job(self, job):
        self.failed_jobs.append(job)


class InitDirJob(PythonOperator):
    def __init__(self, out_dir: Path):
        context = self.init_context(locals())

        def main():
            log_dir.mkdir(parents=True, exist_ok=True)
            data_dir.mkdir(parents=True, exist_ok=True)

        log_dir = Path(out_dir) / 'log'
        data_dir = Path(out_dir) / 'data'

        context.out_fps = [log_dir, data_dir]
        super().__init__(main, context=context)


class AudioDownloadJob(BashOperator):
    def __init__(self, m3u8_url: str, audio_fp: Path):
        context = self.init_context(locals())
        bash_command = f'ffmpeg -i {m3u8_url} {audio_fp}'
        context.out_fps = [audio_fp]
        super().__init__(bash_command, context=context)


class VADJob(PythonOperator):
    def __init__(self, audio_fp: Path, out_fp: Path):
        context = self.init_context(locals())

        def main():
            audio = AudioModel(audio_fp)
            vad_df = VoiceActivityDetector().detect(audio)
            vad_df.to_csv(out_fp, index=False)

        context.in_fps = [audio_fp]
        context.out_fps = [out_fp]
        super().__init__(main, context=context)


class AudioSplitJob(BashOperator):
    def __init__(self, audio_fp: Path, start_sec: int, end_sec: int, out_fp: Path):
        context = self.init_context(locals())

        duration = end_sec - start_sec
        # split and convert to 16-bit WAV as specified by whisper.cpp
        # https://github.com/ggerganov/whisper.cpp
        bash_command = f'ffmpeg -y -ss {start_sec} -i {audio_fp} -t {duration} -ar 16000 -ac 1 -c:a pcm_s16le {out_fp}'

        context.in_fps = [audio_fp]
        context.out_fps = [out_fp]
        super().__init__(bash_command, context=context)


class WhisperJob(BashOperator):
    def __init__(self, wav_fp: Path, log_fp: Path, model: str = 'large'):
        context = self.init_context(locals())

        wav_fp = Path(wav_fp)
        whisper_dir = Path(os.environ['WHISPER_ROOT'])
        bin_fp = whisper_dir / 'main'
        model_fp = whisper_dir / f'models/ggml-{model}.bin'
        result_fp = self.get_result_fp(wav_fp)
        prompt = "静粛に。これより、会議を開きます。"  # prompt to include punctuation marks
        bash_command = f'{bin_fp} --model {model_fp} --language ja --file {wav_fp} --output-csv　--prompt {prompt}'

        context.in_fps = [wav_fp]
        context.out_fps = [result_fp]
        context.log_fp = log_fp
        context.priority = -100  # de-prioritize to download & split all audio first
        super().__init__(bash_command, context=context)

    @staticmethod
    def get_result_fp(wav_fp: [str | Path]) -> Path:
        wav_fp = Path(wav_fp)
        return wav_fp.parent / (wav_fp.name + '.csv')  # whisper.cpp generate this file with `--output-csv`


class MergeWhisperJob(PythonOperator):
    def __init__(self, vad_fp: Path, result_fps: List[Path], out_fp: Path):
        context = self.init_context(locals())

        def main():
            dfs = []
            vad_df = pd.read_csv(vad_fp)
            for _, row in vad_df.iterrows():
                fp = Path(vad_fp).parent / '{}.wav.csv'.format(row['id'])
                df = pd.read_csv(fp, skipinitialspace=True, header=None, names=['start_ms', 'end_ms', 'text'])
                df['start_ms'] += row['start_sec'] * 1000
                df['end_ms'] += row['start_sec'] * 1000
                dfs.append(df)

            out_df = pd.concat(dfs, axis=0).reset_index(drop=True)
            out_df.to_csv(out_fp, index=False)

        context.in_fps = [vad_fp] + result_fps
        context.out_fps = [out_fp]
        super().__init__(main, context=context)
