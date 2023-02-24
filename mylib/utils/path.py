from pathlib import Path

from mylib.utils.constants import ImageSize


class PathHelper:
    def __init__(self, host=None):
        if host:
            root_dir = Path(f'./out_{host}')
        else:
            root_dir = Path('./out')
        self.root_dir = root_dir
        self.s3_dir = 'player'

    def get_sqlite_url(self) -> str:
        sqlite_fp = self.root_dir / 'db/local.db'
        return f'sqlite:///{sqlite_fp}'

    def get_work_dir(self, video_id: int) -> Path:
        return self.root_dir / f'transcript/{video_id}'

    def get_transcript_fp(self, video_id: int) -> Path:
        raw_fp = self.root_dir / f'transcript/{video_id}/data/transcript.csv'
        merged_fp = self.root_dir / f'transcript/{video_id}/data/transcript_merged.csv'
        if merged_fp.exists():
            return merged_fp
        return raw_fp

    def get_clip_fp(self, clip_id: int) -> Path:
        return self.root_dir / f'artifact/clip/{clip_id}.json'

    def get_image_dir(self):
        return self.root_dir / 'artifact/image'

    def get_local_clip_image_fp(self, clip_id: int, size: ImageSize) -> Path:
        return self.root_dir / f'artifact/image/clip/{size.value}/{clip_id}.jpg'

    def get_local_annotation_image_fp(self, annot_id: int, size: ImageSize) -> Path:
        return self.root_dir / f'artifact/image/annotation/{size.value}/{annot_id}.jpg'

    def to_s3_image_fp(self, local_fp: Path) -> Path:
        return self.s3_dir / local_fp.relative_to(self.root_dir / './artifact/image')
