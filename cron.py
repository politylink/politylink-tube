import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video
from mylib.workflow.jobs import ShugiinTvJob, SangiinTvJob, GatsbyDeployJob, GenerateClipsJob, BuildArtifactJob, \
    GenerateImagesJob

LOGGER = logging.getLogger(__name__)

TODAY = datetime.now().date()
TOMORROW = TODAY + timedelta(1)
YESTERDAY = TODAY - timedelta(1)
LOG_DIR = Path('./out/cron/log')
DATE_FORMAT = '%Y-%m-%d'


def get_latest_sid():
    client = SqliteClient()
    videos = client.select_all(Video)
    sids = []
    for video in videos:
        pattern = 'sid=(\d+)'
        match = re.search(pattern, video.page_url)
        if match:
            sids.append(int(match.group(1)))
    return max(sids)


def main():
    jobs = [
        ShugiinTvJob(start_date=YESTERDAY, end_date=TOMORROW, log_fp=LOG_DIR / 'shugiin_tv.log'),
        SangiinTvJob(start_id=get_latest_sid() - 3, log_fp=LOG_DIR / 'sangiin_tv.log'),
        GenerateClipsJob(log_fp=LOG_DIR / 'generate_clips.log'),
        GenerateImagesJob(log_fp=LOG_DIR / 'generate_images.log'),
        BuildArtifactJob(log_fp=LOG_DIR / 'build_artifact.log'),
        GatsbyDeployJob(log_fp=LOG_DIR / 'gatsby.log')
    ]
    for job in jobs:
        LOGGER.info(f'run {job}')
        job.run()


if __name__ == '__main__':
    main()
