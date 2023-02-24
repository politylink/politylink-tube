from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import List

import pandas as pd

from mylib.utils.path import PathHelper
from mylib.workflow.jobs import InitDirJob, AudioDownloadJob, VADJob, AudioSplitJob, WhisperJob, MergeWhisperJob
from mylib.workflow.models import BaseOperator
from mylib.workflow.patch import PatchJobScheduler, PatchRequest
from mylib.workflow.scheduler import JobScheduler

LOGGER = getLogger(__name__)


@dataclass
class TranscribeRequest:
    video_id: int
    datetime: datetime
    m3u8_url: str
    download_only: bool = False


class TranscribeJobScheduler(JobScheduler):
    def __init__(self, path_helper: PathHelper, **kwargs):
        self.path_helper = path_helper
        self.patch_job_scheduler = PatchJobScheduler(path_helper, **kwargs)
        super().__init__(**kwargs)

    def schedule_batch(self, requests: List[TranscribeRequest]) -> List[BaseOperator]:
        jobs = []
        requests = sorted(requests, key=lambda x: x.datetime, reverse=True)  # prioritize the latest when tie-break
        for job_input in requests:
            jobs += self.schedule(job_input)
        jobs = sorted(jobs, key=lambda x: x.context.priority, reverse=True)
        return jobs

    def schedule(self, request: TranscribeRequest) -> List[BaseOperator]:
        work_dir = Path(self.path_helper.get_work_dir(video_id=request.video_id))
        data_dir = work_dir / 'data'
        log_dir = work_dir / 'log'
        mp3_fp = data_dir / 'audio.mp3'
        vad_fp = data_dir / 'vad.csv'
        transcript_fp = data_dir / 'transcript.csv'

        jobs = [
            InitDirJob(work_dir),
            AudioDownloadJob(request.m3u8_url, mp3_fp),
        ]
        if request.download_only:
            return self.return_jobs(jobs)

        jobs.append(VADJob(mp3_fp, vad_fp))
        if not vad_fp.exists():
            return self.return_jobs(jobs)

        result_fps = []
        vad_df = pd.read_csv(vad_fp)
        for _, row in vad_df.iterrows():
            wav_fp = data_dir / '{}.wav'.format(row['id'])
            log_fp = log_dir / 'whisper_{}.log'.format(row['id'])
            result_fp = WhisperJob.get_result_fp(wav_fp)
            result_fps.append(result_fp)

            if not result_fp.exists() or self.force_execute:
                # avoid generating .wav files after cleanup.
                # Maybe we can define a single merged job to avoid such adhoc logic?
                jobs += [
                    AudioSplitJob(audio_fp=mp3_fp, start_sec=row['start_sec'], end_sec=row['end_sec'], out_fp=wav_fp),
                    WhisperJob(wav_fp=wav_fp, log_fp=log_fp)
                ]

        # summarize
        jobs.append(MergeWhisperJob(vad_fp=vad_fp, result_fps=result_fps, out_fp=transcript_fp))
        if not transcript_fp.exists():
            return self.return_jobs(jobs)

        jobs += self.patch_job_scheduler.schedule(PatchRequest(
            video_id=request.video_id,
            datetime=request.datetime
        ))
        return self.return_jobs(jobs)
