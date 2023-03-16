from do_transcribe import build_requests
from mylib.utils.path import PathHelper
from mylib.workflow.jobs import AudioDownloadJob
from mylib.workflow.transcribe import TranscribeJobScheduler


def main():
    scheduler = TranscribeJobScheduler(path_helper=PathHelper())
    requests = build_requests()
    jobs = scheduler.schedule_batch(requests)
    jobs = list(filter(lambda x: isinstance(x, AudioDownloadJob), jobs))[::-1]
    for job in jobs:
        print(job.bash_command)


if __name__ == "__main__":
    main()
