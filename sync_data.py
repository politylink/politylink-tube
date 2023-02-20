import argparse
import logging
from logging import getLogger

from mylib.workflow.sync import SyncDirJob

LOGGER = getLogger(__name__)


def main():
    job = SyncDirJob(src_dir=args.src, dest_dir=args.dest)
    job.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--src', default='mitsuki@mini:~/politylink/politylink-press/out/')
    parser.add_argument('-d', '--dest', default='./out/mini')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
