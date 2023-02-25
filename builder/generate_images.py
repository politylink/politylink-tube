import argparse
import logging
from logging import getLogger

import boto3

from mylib.artifact.image.generator import ImageGenerator, ImageGenerateRequest
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video as VideoDb, Clip as ClipDb, Annotation as AnnotationDb, ClipType
from mylib.utils.constants import ImageSize
from mylib.utils.path import PathHelper

LOGGER = getLogger(__name__)


def build_requests(video_id, sqlite_client: SqliteClient, path_helper: PathHelper):
    requests = []

    if args.clip:
        full_clip = sqlite_client.select_first(ClipDb, type=ClipType.FULL, video_id=video_id)
        for size in [ImageSize.MEDIUM, ImageSize.LARGE]:
            requests.append(ImageGenerateRequest(
                time_sec=full_clip.start_sec + 30,
                size=size,
                local_fp=path_helper.get_local_clip_image_fp(full_clip.id, size)
            ))

    if args.annotation:
        annotations = sqlite_client.select_all(AnnotationDb, video_id=video_id)
        for annotation in annotations:
            for size in [ImageSize.MEDIUM, ImageSize.LARGE]:
                requests.append(ImageGenerateRequest(
                    time_sec=annotation.start_sec + 30,
                    size=size,
                    local_fp=path_helper.get_local_annotation_image_fp(annotation.id, size)
                ))

    for request in requests:
        if args.overwrite:
            request.overwrite = True
        if args.publish:
            request.s3_fp = path_helper.to_s3_image_fp(request.local_fp)

    return requests


def main():
    sqlite_client = SqliteClient(host=args.host)
    path_helper = PathHelper(host=args.host)
    s3_client = boto3.client('s3')

    videos = sqlite_client.select_all(VideoDb)
    LOGGER.info(f'found {len(videos)} videos')

    for video in videos:
        requests = build_requests(video.id, sqlite_client, path_helper)
        LOGGER.info(f'built {len(requests)} requests for {video.m3u8_url}')
        generator = ImageGenerator(m3u8_url=video.m3u8_url, s3_client=s3_client)
        for request in requests:
            generator.generate(request)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-o', '--overwrite', action='store_true')
    parser.add_argument('-p', '--publish', action='store_true')
    parser.add_argument('--clip', action='store_true')
    parser.add_argument('--annotation', action='store_true')
    parser.add_argument('--host', default='')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
