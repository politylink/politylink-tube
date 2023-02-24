from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from mylib.utils.path import PathHelper
from mylib.workflow.jobs import AudioSplitJob, WhisperJob, MergeWhisperJob, ApplyPatchJob, DefinePatchJob
from mylib.workflow.models import BaseOperator
from mylib.workflow.scheduler import JobScheduler


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
        return self.sort_jobs(jobs)

    def schedule(self, request: PatchRequest) -> List[BaseOperator]:
        work_dir = self.path_helper.get_work_dir(request.video_id)
        data_dir = work_dir / 'data'
        log_dir = work_dir / 'log'
        mp3_fp = data_dir / 'audio.mp3'
        transcript_fp = data_dir / 'transcript.csv'
        patch_fp = data_dir / 'patch.csv'
        transcript_patch_fp = data_dir / 'transcript_patch.csv'
        transcript_merged_fp = data_dir / 'transcript_merged.csv'

        jobs = [
            DefinePatchJob(transcript_fp, patch_fp)
        ]
        if not patch_fp.exists():
            return self.return_jobs(jobs)

        result_fps = []
        patch_df = pd.read_csv(patch_fp)
        for _, row in patch_df.iterrows():
            wav_fp = data_dir / '{}.wav'.format(row['id'])
            log_fp = log_dir / 'whisper_{}.log'.format(row['id'])
            result_fp = WhisperJob.get_result_fp(wav_fp)
            result_fps.append(result_fp)

            if not result_fp.exists() or self.force_execute:
                jobs += [
                    AudioSplitJob(audio_fp=mp3_fp, start_sec=row['start_sec'], end_sec=row['end_sec'], out_fp=wav_fp),
                    WhisperJob(wav_fp=wav_fp, log_fp=log_fp)
                ]

        if result_fps:
            jobs.append(MergeWhisperJob(vad_fp=patch_fp, result_fps=result_fps, out_fp=transcript_patch_fp))
            jobs.append(ApplyPatchJob(transcript_fp=transcript_fp, patch_fp=patch_fp,
                                      transcript_patch_fp=transcript_patch_fp, out_fp=transcript_merged_fp))

        return self.return_jobs(jobs)
