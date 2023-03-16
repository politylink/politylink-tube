from dataclasses import dataclass
from pathlib import Path
from typing import List

from mylib.workflow.jobs import ScpJob
from mylib.workflow.models import BaseOperator
from mylib.workflow.transcribe import InitDirJob, WhisperJob


@dataclass
class SupportTranscribeRequest:
    remote_address: str  # {user}@{host}
    remote_wav_fp: [str | Path]
    local_out_dir: [str | Path]


class SupportTranscribeJobScheduler:
    def schedule(self, request: SupportTranscribeRequest) -> List[BaseOperator]:
        local_wav_fp = Path(request.local_out_dir) / "data" / Path(request.remote_wav_fp).name
        local_result_fp = WhisperJob.get_result_fp(local_wav_fp)
        local_log_fp = Path(request.local_out_dir) / "log" / "whisper_{}.log".format(Path(request.remote_wav_fp).stem)

        remote_wav_fp = request.remote_wav_fp
        remote_result_fp = WhisperJob.get_result_fp(request.remote_wav_fp)
        remote_log_fp = Path(request.remote_wav_fp).parent.parent / "log" / local_log_fp.name

        jobs = [
            InitDirJob(request.local_out_dir),
            ScpJob(f"{request.remote_address}:{remote_wav_fp}", local_wav_fp),
            WhisperJob(local_wav_fp, local_log_fp),
            ScpJob(local_result_fp, f"{request.remote_address}:{remote_result_fp}"),
            ScpJob(local_log_fp, f"{request.remote_address}:{remote_log_fp}"),
        ]
        return jobs
