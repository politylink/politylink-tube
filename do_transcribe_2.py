import argparse
import logging
from pathlib import Path
from typing import List

import pandas as pd

from mylib.workflow.models import StatusCode
from mylib.workflow.transcribe import TranscribeRequest, TranscribeJobScheduler

LOGGER = logging.getLogger(__name__)


def build_requests(fp) -> List[TranscribeRequest]:
    requests = []
    df = pd.read_csv(fp)
    for _, row in df.iterrows():
        requests.append(TranscribeRequest(
            m3u8_url=row['url'],
            out_dir=Path('./out/transcript') / str(row['id'])
        ))
    return requests


def main():
    scheduler = TranscribeJobScheduler()
    while True:
        requests = build_requests('./data/video.csv')
        jobs = scheduler.schedule_batch(requests)
        LOGGER.info(f'found {len(jobs)} jobs')
        if not jobs:
            break

        job = jobs[0]
        LOGGER.info(f'run {job}')
        result = job.run()
        if result != StatusCode.SUCCESS:
            LOGGER.error(f'failed to execute {job}')
            scheduler.record_failed_job(job)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
