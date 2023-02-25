import os
from datetime import date
from logging import getLogger
from pathlib import Path
from typing import List

import pandas as pd

from mylib.audio.models import AudioModel
from mylib.audio.transcript.loop import TranscriptLoopDetector
from mylib.audio.vad import VoiceActivityDetector
from mylib.utils.whisper import read_whisper_csv
from mylib.workflow.models import BashOperator, PythonOperator

LOGGER = getLogger(__name__)


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
            vad_df['id'] = [str(i) for i in range(1, len(vad_df) + 1)]
            vad_df = vad_df[['id', 'start_sec', 'end_sec']]
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
                df = read_whisper_csv(fp)
                df['start_ms'] += row['start_sec'] * 1000
                df['end_ms'] += row['start_sec'] * 1000
                dfs.append(df)

            out_df = pd.concat(dfs, axis=0).reset_index(drop=True)
            out_df.to_csv(out_fp, index=False)

        context.in_fps = [vad_fp] + result_fps
        context.out_fps = [out_fp]
        super().__init__(main, context=context)


class DefinePatchJob(PythonOperator):
    def __init__(self, transcript_fp: Path, out_fp: Path):
        context = self.init_context(locals())

        def main():
            transcript_df = pd.read_csv(transcript_fp)
            loop_df = TranscriptLoopDetector().detect(transcript_df, duration_sec_thresh=30)
            loop_df['id'] = [f'p{i}' for i in range(1, len(loop_df) + 1)]
            loop_df = loop_df[['id', 'start_sec', 'end_sec', 'text']]
            loop_df.to_csv(out_fp, index=False)

        context.in_fps = [transcript_fp]
        context.out_fps = [out_fp]
        super().__init__(main, context=context)


class ApplyPatchJob(PythonOperator):
    def __init__(self, transcript_fp: Path, patch_fp: Path, transcript_patch_fp: Path, out_fp: Path):
        context = self.init_context(locals())

        def main():
            transcript_df = pd.read_csv(transcript_fp)
            patch_df = pd.read_csv(patch_fp)
            transcript_patch_df = pd.read_csv(transcript_patch_fp)

            transcript_masked_df = transcript_df
            for start_sec, end_sec in zip(patch_df['start_sec'], patch_df['end_sec']):
                mask = (transcript_df['start_ms'] >= start_sec * 1000) & (transcript_df['end_ms'] <= end_sec * 1000)
                transcript_masked_df = transcript_df[~mask]

            out_df = pd.concat([transcript_masked_df, transcript_patch_df])
            out_df = out_df.sort_values(by='start_ms')
            out_df['start_ms'] = out_df['start_ms'].astype(int)
            out_df['end_ms'] = out_df['end_ms'].astype(int)
            out_df = out_df[['start_ms', 'end_ms', 'text']]
            out_df.to_csv(out_fp, index=False)

        context.in_fps = [transcript_fp, patch_fp, transcript_patch_fp]
        context.out_fps = [out_fp]
        super().__init__(main, context=context)


class ScpJob(BashOperator):
    def __init__(self, src_fp: [Path | str], trg_fp: [Path | str]):
        context = self.init_context(locals())
        bash_command = f'scp {src_fp} {trg_fp}'
        context.in_fps = [src_fp] if ('@' not in str(src_fp)) else []  # check if sending from local
        super().__init__(bash_command, context=context)


class SyncDirJob(BashOperator):
    def __init__(self, src_dir: str, dest_dir: str):
        context = self.init_context(locals())

        bash_command = f"rsync -a -v --exclude '*.wav' --exclude '*.mp3' --exclude '*.mp4' {src_dir} {dest_dir}"

        super().__init__(bash_command=bash_command, context=context)


class SyncFileJob(BashOperator):
    def __init__(self, src_file: str, dest_file: str):
        context = self.init_context(locals())

        bash_command = f"scp {src_file} {dest_file}"

        super().__init__(bash_command=bash_command, context=context)


class ShugiinTvJob(BashOperator):
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start_date: date, end_date: date, log_fp: [str | Path], cache_enabled=False):
        context = self.init_context(locals())

        start_date = start_date.strftime(self.DATE_FORMAT)
        end_date = end_date.strftime(self.DATE_FORMAT)
        bash_command = f'poetry run scrapy crawl shugiin_tv -a start_date={start_date} -a end_date={end_date} --set HTTPCACHE_ENABLED={cache_enabled}'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, context=context)


class SangiinTvJob(BashOperator):
    def __init__(self, start_id: int, log_fp: [str | Path], cache_enabled=False):
        context = self.init_context(locals())

        bash_command = f'poetry run scrapy crawl sangiin_tv -a start_id={start_id} --set HTTPCACHE_ENABLED={cache_enabled}'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, context=context)


class GatsbyDeployJob(BashOperator):
    def __init__(self, log_fp):
        context = self.init_context(locals())

        bash_command = 'npm run deploy'
        cwd = Path().home() / 'politylink/politylink-player'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, cwd=cwd, context=context)


class GenerateClipsJob(BashOperator):
    def __init__(self, log_fp):
        context = self.init_context(locals())

        bash_command = 'poetry run python generate_clips.py'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, context=context)


class GenerateImagesJob(BashOperator):
    def __init__(self, log_fp):
        context = self.init_context(locals())

        bash_command = 'poetry run python generate_images.py --clip --publish'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, context=context)


class BuildArtifactJob(BashOperator):
    def __init__(self, log_fp):
        context = self.init_context(locals())

        bash_command = 'poetry run python build_artifact.py'

        context.log_fp = log_fp
        super().__init__(bash_command=bash_command, context=context)
