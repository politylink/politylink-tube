import argparse
import logging
from logging import getLogger

from mylib.workflow.jobs import SyncDirJob

LOGGER = getLogger(__name__)


def main():
    jobs = [
        SyncDirJob(
            src_dir=f"mitsuki@{args.host}:~/politylink/politylink-tube/builder/out/", dest_dir=f"./out_{args.host}"
        )
    ]
    for job in jobs:
        print(job.bash_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--host", required=True)
    parser.add_argument("--run", action="store_true", help="dryrun by default")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
