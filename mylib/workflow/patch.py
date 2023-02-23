from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

from mylib.audio.transcript.loop import TranscriptLoopDetector
from mylib.utils.path import PathHelper
from mylib.workflow.models import BaseOperator, PythonOperator
from mylib.workflow.scheduler import JobScheduler
from mylib.workflow.transcribe import AudioSplitJob, WhisperJob, MergeWhisperJob


@dataclass
class PatchRequest:
    video_id: int
    datetime: datetime


class PatchJobScheduler(JobScheduler):

    def __init__(self, path_helper: PathHelper, **kwargs):
        self.path_helper = path_helper
        super().__init__(**kwargs)

    def schedule_batch(self, requests: List[PatchRequest]) -> List[BaseOperator]:
        jobs = []
        requests = sorted(requests, key=lambda x: x.datetime, reverse=True)  # prioritize the latest when tie-break
        for job_input in requests:
            jobs += self.schedule(job_input)
        jobs = sorted(jobs, key=lambda x: x.context.priority, reverse=True)
        return jobs

    def schedule(self, request: PatchRequest) -> List[BaseOperator]:
        work_dir = self.path_helper.get_work_dir(request.video_id)
        data_dir = work_dir / 'data'
        log_dir = work_dir / 'log'
        mp3_fp = data_dir / 'audio.mp3'
        transcript_fp = data_dir / 'transcript.csv'
        patch_fp = data_dir / 'patch.csv'
        patch_transcript_fp = data_dir / 'transcript_patch.csv'

        jobs = [
            DefinePatchJob(transcript_fp, patch_fp)
        ]

        if patch_fp.exists():
            patch_df = pd.read_csv(patch_fp)

            result_fps = []
            for _, row in patch_df.iterrows():
                wav_fp = data_dir / '{}.wav'.format(row['id'])
                jobs.append(
                    AudioSplitJob(audio_fp=mp3_fp, start_sec=row['start_sec'], end_sec=row['end_sec'], out_fp=wav_fp))
                log_fp = log_dir / 'whisper_{}.log'.format(row['id'])
                jobs.append(WhisperJob(wav_fp=wav_fp, log_fp=log_fp))
                result_fps.append(WhisperJob.get_result_fp(wav_fp))

            if result_fps:
                jobs.append(MergeWhisperJob(vad_fp=patch_fp, result_fps=result_fps, out_fp=patch_transcript_fp))

        return self.sort_jobs(self.filter_jobs(jobs=jobs))


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
