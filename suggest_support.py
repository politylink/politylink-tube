from pathlib import Path

from do_transcribe import build_requests
from mylib.workflow.transcribe import TranscribeJobScheduler, WhisperJob


def main():
    scheduler = TranscribeJobScheduler()
    requests = build_requests()
    jobs = scheduler.schedule_batch(requests)
    whisper_jobs = list(filter(lambda x: isinstance(x, WhisperJob), jobs))[::-1]
    for job in whisper_jobs:
        wav_fp = Path(job.context.class_kwargs['wav_fp']).absolute()
        print(wav_fp)


if __name__ == '__main__':
    main()
