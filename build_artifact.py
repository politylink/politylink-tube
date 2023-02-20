import argparse
import logging
from logging import getLogger

from mylib.artifact.builders import ClipArtifactBuilder
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip, ClipType

LOGGER = getLogger(__name__)


def main():
    sqlite_client = SqliteClient()
    clips = sqlite_client.select_all(Clip, type=ClipType.FULL)
    builder = ClipArtifactBuilder(sqlite_client)

    for clip in clips:
        artifact = builder.build(clip.id)
        fp = f'./out/artifact/clip/{clip.id}.json'
        with open(fp, 'w') as f:
            f.write(artifact.json(ensure_ascii=False, indent=2, by_alias=True))
        LOGGER.info(f'stored {fp}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
