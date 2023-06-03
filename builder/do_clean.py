import argparse
import glob
import logging
from logging import getLogger
from pathlib import Path

from mylib.workflow.jobs import CleanDirJob

LOGGER = getLogger(__name__)


def main():
    dirs = glob.glob('./out/transcript/*')
    LOGGER.info(f'found {len(dirs)} dirs')
    for dir in dirs:
        job = CleanDirJob(Path(dir), run=args.run)
        job.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main()
