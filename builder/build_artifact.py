import argparse
import logging
from logging import getLogger

from mylib.artifact.builders import ClipArtifactBuilder
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip, ClipType
from mylib.utils.path import PathHelper

LOGGER = getLogger(__name__)


def main():
    path_helper = PathHelper(host=args.host)
    sqlite_client = SqliteClient(path_helper.get_sqlite_url())
    clips = sqlite_client.select_all(Clip, type=ClipType.FULL)
    builder = ClipArtifactBuilder(sqlite_client, path_helper)

    updated_fps = []
    for clip in clips:
        artifact = builder.build(clip.id)

        if not len(artifact.transcript):
            LOGGER.info(f"{clip.id} does not have transcript yet.")
            continue

        fp = path_helper.get_clip_fp(clip.id)
        if fp.exists():
            artifact_prev = open(fp, "r").read()
            artifact_new = artifact.json(ensure_ascii=False, indent=2, by_alias=True)
            if artifact_prev == artifact_new:
                LOGGER.info(f"{fp} is fresh.")
                continue

        with open(fp, "w") as f:
            f.write(artifact.json(ensure_ascii=False, indent=2, by_alias=True))
        LOGGER.info(f"saved {fp}")
        updated_fps.append(fp)
    LOGGER.info(f"updated total {len(updated_fps)} files.")

    diff_fp = path_helper.get_artifact_diff_fp()
    with open(diff_fp, "w") as f:
        for fp in updated_fps:
            f.write(f"{fp}\n")
    LOGGER.info(f"saved diff in {diff_fp}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--host", default="")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
