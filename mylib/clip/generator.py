from pathlib import Path

import pandas as pd

from mylib.clip.key import ClipKey
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip, Video, Annotation, ClipType


class ClipGenerator:

    def __init__(self, sqlite_client: SqliteClient):
        self.sqlite_client = sqlite_client

    def generate(self, video_id):
        video = self.sqlite_client.select_first(Video, id=video_id)
        annotations = self.sqlite_client.select_all(Annotation, video_id=video_id)

        vad_fp = Path(f'./out/transcript/{video_id}/data/vad.csv')
        if not vad_fp.exists():
            return []
        vad_df = pd.read_csv(vad_fp)
        video_start_sec = vad_df['start_sec'].min()
        video_end_sec = vad_df['end_sec'].max()

        clips = [
            self.generate_full_clip(
                video=video,
                start_sec=video_start_sec,
                end_sec=video_end_sec
            )
        ]
        for i, annotation in enumerate(annotations):
            if (i + 1) < len(annotations):
                end_sec = annotations[i + 1].start_sec + 10  # add 10 sec buffer at the end
            else:
                end_sec = video_end_sec
            clips.append(self.generate_speaker_clip(
                video=video,
                annotation=annotation,
                end_sec=end_sec
            ))
        return clips

    def generate_full_clip(self, video: Video, start_sec: float, end_sec: float) -> Clip:
        key = ClipKey(video_ids=[video.id]).serialize()
        title = ' '.join([
            video.datetime.strftime('%Y年%m月%d日'),
            video.house_name,
            video.meeting_name
        ])
        return Clip(
            key=key,
            video_id=video.id,
            start_sec=start_sec,
            end_sec=end_sec,
            title=title,
            type=ClipType.FULL
        )

    def generate_speaker_clip(self, video: Video, annotation: Annotation, end_sec: float) -> Clip:
        key = ClipKey(video_ids=[video.id], annotation_ids=[annotation.id]).serialize()
        title = ' '.join([
            video.datetime.strftime('%Y年%m月%d日'),
            annotation.speaker_name,
            video.meeting_name
        ])
        return Clip(
            key=key,
            video_id=video.id,
            start_sec=annotation.start_sec,
            end_sec=end_sec,
            title=title,
            type=ClipType.SPEAKER
        )
