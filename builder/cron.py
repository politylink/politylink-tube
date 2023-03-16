import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video
from mylib.utils.path import PathHelper
from mylib.workflow.jobs import (
    ShugiinTvJob,
    SangiinTvJob,
    GatsbyDeployJob,
    GenerateClipsJob,
    BuildArtifactJob,
    GenerateImagesJob,
)

LOGGER = logging.getLogger(__name__)

TODAY = datetime.now().date()
TOMORROW = TODAY + timedelta(1)
YESTERDAY = TODAY - timedelta(1)
LOG_DIR = Path("./out/cron/log")
DATE_FORMAT = "%Y-%m-%d"


def get_start_sid():
    def is_date_match(video, date):
        return video.datetime.date() == date

    def get_sid(video):
        pattern = "sid=(\d+)"
        match = re.search(pattern, video.page_url)
        return int(match.group(1))

    client = SqliteClient()
    videos = client.select_all(Video, house_name="参議院")
    videos_today = list(filter(lambda x: is_date_match(x, TODAY), videos))

    if videos_today:
        return min(map(get_sid, videos_today))  # re-crawl all today's video
    else:
        return max(map(get_sid, videos)) + 1  # wait for new video


def main():
    jobs = [
        ShugiinTvJob(start_date=YESTERDAY, end_date=TOMORROW, log_fp=LOG_DIR / "shugiin_tv.log"),
        SangiinTvJob(start_id=get_start_sid(), log_fp=LOG_DIR / "sangiin_tv.log"),
        GenerateClipsJob(log_fp=LOG_DIR / "generate_clips.log"),
        GenerateImagesJob(log_fp=LOG_DIR / "generate_images.log"),
        BuildArtifactJob(log_fp=LOG_DIR / "build_artifact.log"),
    ]
    for job in jobs:
        LOGGER.info(f"run {job}")
        job.run()

    diff_fp = PathHelper().get_artifact_diff_fp()
    if diff_fp.stat().st_size == 0:
        LOGGER.info("skip deployment as artifact is fresh.")
        return

    job = GatsbyDeployJob(log_fp=LOG_DIR / "gatsby.log")
    LOGGER.info(f"run {job}")
    job.run()


if __name__ == "__main__":
    main()
