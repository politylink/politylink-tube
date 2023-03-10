from pathlib import Path

from do_transcribe import build_requests
from mylib.utils.path import PathHelper
from mylib.workflow.transcribe import TranscribeJobScheduler, WhisperJob


def main():
    scheduler = TranscribeJobScheduler(path_helper=PathHelper())
    requests = build_requests()
    jobs = scheduler.schedule_batch(requests)
    jobs = list(filter(lambda x: isinstance(x, WhisperJob), jobs))[::-1]
    for job in jobs:
        wav_fp = Path(job.context.class_kwargs['wav_fp']).absolute()
        print(wav_fp)


if __name__ == '__main__':
    main()
