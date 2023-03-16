import argparse
import logging
from logging import getLogger

import boto3

from mylib.artifact.image.generator import ImageGenerator, ImageGenerateRequest, ImageGenerateResponse
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video as VideoDb, Clip as ClipDb, Annotation as AnnotationDb, ClipType
from mylib.utils.constants import ImageSize
from mylib.utils.path import PathHelper

LOGGER = getLogger(__name__)


def build_requests(sqlite_client: SqliteClient, path_helper: PathHelper, overwrite=False):
    requests = []

    videos = sqlite_client.select_all(VideoDb)
    m3u8_url_map = dict([(video.id, video.m3u8_url) for video in videos])

    if args.clip:
        clips = sqlite_client.select_all(ClipDb, type=ClipType.FULL)
        for clip in clips:
            for size in [ImageSize.MEDIUM, ImageSize.LARGE]:
                requests.append(
                    ImageGenerateRequest(
                        m3u8_url=m3u8_url_map[clip.video_id],
                        time_sec=clip.start_sec + 30,
                        size=size,
                        local_fp=path_helper.get_local_clip_image_fp(clip.id, size),
                        overwrite=overwrite,
                    )
                )

    if args.annotation:
        annotations = sqlite_client.select_all(AnnotationDb)
        for annotation in annotations:
            for size in [ImageSize.MEDIUM, ImageSize.LARGE]:
                requests.append(
                    ImageGenerateRequest(
                        m3u8_url=m3u8_url_map[annotation.video_id],
                        time_sec=annotation.start_sec + 30,
                        size=size,
                        local_fp=path_helper.get_local_annotation_image_fp(annotation.id, size),
                        overwrite=overwrite,
                    )
                )

    requests = list(sorted(requests, key=lambda x: x.m3u8_url))  # group by url to improve ImageGenerator perf

    return requests


def main():
    sqlite_client = SqliteClient(host=args.host)
    path_helper = PathHelper(host=args.host)
    s3_client = boto3.client("s3")
    generator = ImageGenerator(s3_client=s3_client)

    requests = build_requests(sqlite_client, path_helper, overwrite=args.overwrite)
    LOGGER.info(f"found {len(requests)} requests")

    for request in requests:
        response = generator.generate(request)
        if args.publish and response == ImageGenerateResponse.SUCCESS:
            generator.publish(local_fp=request.local_fp, s3_fp=path_helper.to_s3_image_fp(request.local_fp))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--overwrite", action="store_true")
    parser.add_argument("-p", "--publish", action="store_true")
    parser.add_argument("--clip", action="store_true")
    parser.add_argument("--annotation", action="store_true")
    parser.add_argument("--host", default="")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
