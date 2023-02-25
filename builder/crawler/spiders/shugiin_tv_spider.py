import re
from datetime import datetime, timedelta
from logging import getLogger

import scrapy

from crawler.spiders import TvSpiderTemplate
from mylib.scrape.utils import extract_text, extract_href
from mylib.sqlite.schema import Video, Annotation
from mylib.utils import substrptime

LOGGER = getLogger(__name__)


class ShugiinTvSpider(TvSpiderTemplate):
    name = 'shugiin_tv'

    def __init__(self, start_date, end_date, **kwargs):
        def to_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date()

        super().__init__(**kwargs)
        start_date = to_date(start_date)
        end_date = to_date(end_date)
        self.start_urls = []
        for i in range((end_date - start_date).days):
            self.start_urls.append(self.build_start_url(start_date + timedelta(i)))

    @staticmethod
    def build_start_url(date):
        return 'https://www.shugiintv.go.jp/jp/index.php?ex=VL&u_day={}'.format(date.strftime('%Y%m%d'))

    @staticmethod
    def build_video_url(deli_id):
        return 'https://www.shugiintv.go.jp/jp/index.php?ex=VL&deli_id={}'.format(deli_id)

    def parse(self, response, **kwargs):
        deli_ids = []
        h_pages = []
        for a in response.xpath('//table//td/a'):
            href = a.xpath('./@href').get()
            text = a.xpath('./text()').get()
            match = re.search('deli_id=([0-9]+)', href)
            if match:
                deli_ids.append(match.group(1))
            if text == '次の結果':
                match = re.search("h_page.value='([0-9]+)'", href)
                if match:
                    h_pages.append(match.group(1))
        LOGGER.info(f'scraped {len(deli_ids)} deli_ids from {response.url}: {deli_ids}')
        LOGGER.info(f'scraped {len(h_pages)} h_pages from {response.url}: {h_pages}')

        for deli_id in deli_ids:
            yield response.follow(
                self.build_video_url(deli_id),
                callback=self.parse_video
            )
        for h_page in h_pages:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'h_page': h_page},
                callback=self.parse
            )

    def parse_video(self, response):
        try:
            video = self.scrape_video(response)
            annotations = self.scrape_annotations(response)
            self.upsert_video_and_annotations(video, annotations)
            LOGGER.info(f'saved video with {len(annotations)} annotations from {response.url}')
        except Exception:
            LOGGER.exception(f'failed to parse video from {response.url}')
            return

    def scrape_video(self, response):
        video = Video(
            page_url=response.url,
            m3u8_url=self.get_m3u8_url(response),
            house_name='衆議院'
        )
        for row in response.xpath('//div[@id="library"]/table//tr'):
            tds = row.xpath('./td')
            key = extract_text(tds[1]).strip()
            val = extract_text(tds[3]).split()[0]  # drop () after space
            if key == '開会日':
                video.datetime = substrptime(val, '%Y年%m月%d日')
            elif key == '会議名':
                video.meeting_name = val

        return video

    def scrape_annotations(self, response):
        annotations = []
        for a in response.xpath('//table').xpath('.//a'):
            speaker_name, speaker_info = self.parse_speaker_text(extract_text(a))
            start_sec = float(re.search(r'time=([\d.]+)', extract_href(a)).group(1))  # get time param
            annotations.append(Annotation(
                speaker_name=speaker_name,
                speaker_info=speaker_info,
                start_sec=start_sec,
                producer='shugiin'
            ))
        return annotations
