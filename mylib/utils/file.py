from pathlib import Path


class FilePathHelper:
    def __init__(self, host=''):
        if host:
            root_dir = Path(f'./out_{host}')
        else:
            root_dir = Path('./out')
        self.root_dir = root_dir

    def get_transcript_fp(self, video_id: int):
        return self.root_dir / f'transcript/{video_id}/data/transcript.json'

    def get_clip_fp(self, clip_id: int):
        return self.root_dir / f'artifact/clip/{clip_id}.json'
