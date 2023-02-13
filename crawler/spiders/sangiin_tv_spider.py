from logging import getLogger
from typing import List

import scrapy

from crawler.spiders import TvSpiderTemplate
from mylib.scrape.utils import scrape_dl, extract_text, extract_href
from mylib.sqlite.schema import Video, Annotation
from mylib.utils import substrptime

LOGGER = getLogger(__name__)


class SangiinTvSpider(TvSpiderTemplate):
    name = 'sangiin_tv'

    def __init__(self, start_id=0, end_id=100000, failure_in_row_limit=3, **kwargs):
        super().__init__(**kwargs)
        self.start_id = int(start_id)
        self.current_id = int(start_id)
        self.end_id = end_id
        self.failure_in_row_limit = failure_in_row_limit
        self.failure_in_row = 0

    def build_next_url(self):
        url = 'https://www.webtv.sangiin.go.jp/webtv/detail.php?sid={}'.format(self.current_id)
        self.current_id += 1
        return url

    def start_requests(self):
        yield scrapy.Request(self.build_next_url(), self.parse)

    def parse(self, response, **kwargs):
        try:
            video = self.scrape_video(response)
            annotations = self.scrape_annotations(response)
            self.merge_video_and_annotations(video, annotations)
            LOGGER.info(f'saved video with {len(annotations)} annotations from {response.url}')
        except Exception:
            if '項目が不正です。' not in response.text:
                LOGGER.exception(f'failed to parse {response.url}')
            self.failure_in_row += 1
        else:
            self.failure_in_row = 0

        if self.failure_in_row >= self.failure_in_row_limit:
            LOGGER.info('reached failure limit')
            return
        if self.current_id >= self.end_id:
            LOGGER.info('reached end id')
            return
        yield response.follow(self.build_next_url(), callback=self.parse)

    def scrape_video(self, response) -> Video:
        video = Video(
            page_url=response.url,
            m3u8_url=self.get_m3u8_url(response)
        )
        info_dict = scrape_dl(response.css('div#detail-contents-inner').xpath('.//dl'))
        for key, val in info_dict.items():
            if key == '開会日':
                video.datetime = substrptime(val, '%Y年%m月%d日')
            if key == '会議名':
                video.meeting_name = val
        return video

    def scrape_annotations(self, response) -> List[Annotation]:
        annotations = []
        for li in response.css('div#detail-contents-inner').xpath('.//li'):
            speaker_name, speaker_info = self.parse_speaker_text(extract_text(li))
            start_sec = float(extract_href(li)[1:])  # drop "#"
            annotations.append(Annotation(
                speaker_name=speaker_name,
                speaker_info=speaker_info,
                start_sec=start_sec,
                producer=self.__class__.__name__,
            ))
        return annotations
