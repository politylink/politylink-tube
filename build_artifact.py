import argparse
import logging
from logging import getLogger

from mylib.artifact.builders import ClipArtifactBuilder
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip, ClipType
from mylib.utils.file import FilePathHelper

LOGGER = getLogger(__name__)


def main():
    file_path_helper = FilePathHelper(host=args.host)
    sqlite_client = SqliteClient(file_path_helper.get_sqlite_url())
    clips = sqlite_client.select_all(Clip, type=ClipType.FULL)
    builder = ClipArtifactBuilder(sqlite_client, file_path_helper)

    for clip in clips:
        artifact = builder.build(clip.id)
        fp = file_path_helper.get_clip_fp(clip.id)
        with open(fp, 'w') as f:
            f.write(artifact.json(ensure_ascii=False, indent=2, by_alias=True))
        LOGGER.info(f'saved {fp}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--host', default='')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
