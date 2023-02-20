import argparse
import logging
from logging import getLogger

from mylib.workflow.sync import SyncDirJob, SyncFileJob

LOGGER = getLogger(__name__)


def main():
    jobs = [
        SyncDirJob(src_dir='mitsuki@mini:~/politylink/politylink-press/out/', dest_dir='./out_mini'),
        SyncFileJob(src_file='mitsuki@mini:~/politylink/politylink-press/db/local.db', dest_file='./db/mini.db')
    ]
    for job in jobs:
        print(job.bash_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
