from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

import cv2

from mylib.utils.constants import ImageSize

LOGGER = getLogger(__name__)

IMAGE_DSIZE_MAP = {
    ImageSize.SMALL: (160, 90),
    ImageSize.MEDIUM: (320, 180),
    ImageSize.LARGE: (640, 360)
}


@dataclass
class ImageGenerateRequest:
    m3u8_url: str = ''
    time_sec: float = 0.
    local_fp: Path = ''
    size: ImageSize = ImageSize.UNKNOWN
    dsize: tuple = None  # (width, height)
    overwrite: bool = False


class ImageGenerator:
    def __init__(self, s3_client=None):
        self.s3_client = s3_client
        self.m3u8_url = None
        self.cap = None

    def _load(self, m3u8_url: str):
        if self.m3u8_url == m3u8_url:
            return
        LOGGER.debug(f'load {m3u8_url}')
        self.m3u8_url = m3u8_url
        self.cap = cv2.VideoCapture(m3u8_url)

    def generate(self, request: ImageGenerateRequest):
        if request.local_fp and request.local_fp.exists() and not request.overwrite:
            LOGGER.info(f'{request.local_fp} already exists')
            return

        self._load(request.m3u8_url)
        frame_number = int(self.cap.get(cv2.CAP_PROP_FPS) * request.time_sec)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        _, image = self.cap.read()

        if not request.dsize and request.size != ImageSize.UNKNOWN:
            request.dsize = IMAGE_DSIZE_MAP[request.size]
        if request.dsize:
            image = cv2.resize(image, dsize=request.dsize)

        request.local_fp.parent.mkdir(exist_ok=True, parents=True)
        cv2.imwrite(str(request.local_fp), image)
        LOGGER.info(f'saved {request.local_fp}')

    def publish(self, local_fp: Path, s3_fp: Path):
        if not self.s3_client:
            raise ValueError(f'you need s3 client to upload to {s3_fp}')
        if not local_fp.exists():
            raise ValueError(f'you need to generate {local_fp} first to upload to {s3_fp}')

        self.s3_client.upload_file(
            str(local_fp),
            'politylink',
            str(s3_fp),
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        LOGGER.info(f'uploaded {local_fp} to {s3_fp}')
