import re
from logging import getLogger
from typing import List

import scrapy

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video, Annotation

LOGGER = getLogger(__name__)


class SpiderTemplate(scrapy.Spider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sqlite_client = SqliteClient()


class TvSpiderTemplate(SpiderTemplate):

    def get_m3u8_url(self, response):
        pattern = 'https?://.*playlist.m3u8'
        url = re.search(pattern, response.text).group()
        url = url.replace('http://', 'https://')
        return url

    def merge_video_and_annotations(self, video: Video, annotations: List[Annotation]):
        self.sqlite_client.upsert(video, keys=['m3u8_url'])
        video_id = self.sqlite_client.select_first(Video, m3u8_url=video.m3u8_url).id
        for annotation in annotations:
            annotation.video_id = video_id
            self.sqlite_client.upsert(annotation, keys=['video_id', 'start_sec', 'producer'])

    @staticmethod
    def parse_speaker_text(text):
        pattern = r'([^()]+)\((.+)\)'
        match = re.match(pattern, text)
        if not match:
            LOGGER.warning(f'{text} does not match speaker pattern')
            return text, ''
        name, info = match.group(1), match.group(2)
        return name, info
