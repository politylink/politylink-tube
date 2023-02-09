import argparse
import logging
from pathlib import Path

import pandas as pd

from mylib.workflow.models import StatusCode
from mylib.workflow.transcribe import TranscribeJobInput, TranscribeJobScheduler

LOGGER = logging.getLogger(__name__)


def main():
    df = pd.read_csv('./data/video.csv')

    job_inputs = []
    for _, row in df.iterrows():
        job_inputs.append(TranscribeJobInput(
            m3u8_url=row['url'],
            out_dir=Path('./out/transcript') / str(row['id'])
        ))

    scheduler = TranscribeJobScheduler()
    while True:
        jobs = scheduler.schedule(job_inputs)
        LOGGER.info(f'found {len(jobs)} jobs')
        if not jobs:
            return

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
