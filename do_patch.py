import argparse
import logging
from typing import List

import time

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video
from mylib.utils.path import PathHelper
from mylib.workflow.models import StatusCode
from mylib.workflow.patch import PatchRequest, PatchJobScheduler

LOGGER = logging.getLogger(__name__)

LOG_DATE_FORMAT = "%Y-%m-%d %I:%M:%S"
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'


def build_requests() -> List[PatchRequest]:
    requests = []
    client = SqliteClient(host=args.host)
    if args.video:
        video_ids = list(map(int, args.video.split(',')))
        videos = client.session.query(Video).filter(Video.id.in_(video_ids)).all()
    else:
        videos = client.select_all(Video)
    for video in videos:
        requests.append(PatchRequest(
            video_id=video.id,
            datetime=video.datetime,
        ))
    return requests


def main():
    path_helper = PathHelper(host=args.host)
    scheduler = PatchJobScheduler(path_helper=path_helper, force_execute=args.force)
    requests = build_requests()
    while True:
        jobs = scheduler.schedule_batch(requests)
        LOGGER.info(f'found {len(jobs)} jobs')

        if not jobs:
            time.sleep(300)
            continue

        job = jobs[0]
        LOGGER.info(f'run {job}')
        status_code = job.run(force_execute=args.force)

        if status_code != StatusCode.SUCCESS:
            LOGGER.error(f'failed to execute {job}')
        scheduler.record(job, status_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--host')
    parser.add_argument('--video', help='comma separated list of video ids')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        datefmt=LOG_DATE_FORMAT, format=LOG_FORMAT)
    main()
