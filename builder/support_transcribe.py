import argparse
import logging
from pathlib import Path
from typing import List

import pandas as pd

from mylib.workflow.models import StatusCode
from mylib.workflow.support import SupportTranscribeRequest, SupportTranscribeJobScheduler

LOGGER = logging.getLogger(__name__)


def build_requests(fp) -> List[SupportTranscribeRequest]:
    requests = []
    df = pd.read_csv(fp)
    for _, row in df.iterrows():
        requests.append(
            SupportTranscribeRequest(
                remote_address="mitsuki@intel",
                remote_wav_fp=row["wav"],
                local_out_dir="./out/transcript/{}".format(Path(row["wav"]).parent.parent.name),
            )
        )
    return requests


def main():
    scheduler = SupportTranscribeJobScheduler()
    requests = build_requests("./data/support.csv")
    for request in requests:
        jobs = scheduler.schedule(request)
        for job in jobs:
            LOGGER.info(f"run {job}")
            result = job.run()
            if result != StatusCode.SUCCESS:
                LOGGER.error(f"failed to execute {job}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
