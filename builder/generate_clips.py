import argparse
import logging
from logging import getLogger

from mylib.clip.generator import ClipGenerator
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video

LOGGER = getLogger(__name__)


def main():
    sqlite_client = SqliteClient()
    generator = ClipGenerator(sqlite_client)
    videos = sqlite_client.select_all(Video)
    LOGGER.info(f"found {len(videos)} videos to process")

    for video in videos:
        clips = generator.generate(video.id)
        LOGGER.info(f"generated {len(clips)} clips for {video.id}")
        for clip in clips:
            sqlite_client.upsert(clip, keys=["key"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
