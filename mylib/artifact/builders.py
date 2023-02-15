import re
from pathlib import Path

import numpy as np
import pandas as pd

from mylib.artifact.helpers import TranscriptBuildHelper
from mylib.artifact.models import Video, Clip, Transcript, Word
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip as ClipDb, Video as VideoDb


class ClipArtifactBuilder:
    def __init__(self, sqlite_client: SqliteClient):
        self.sqlite_client = sqlite_client
        self.transcript_builder = TranscriptArtifactBuilder()

    def build(self, clip_id) -> Clip:
        clip_db = self.sqlite_client.select_first(ClipDb, id=clip_id)
        video_db = self.sqlite_client.select_first(VideoDb, id=clip_db.video_id)

        video = Video(
            url=video_db.m3u8_url,
            start=clip_db.start_sec,
            end=clip_db.end_sec
        )
        transcript = self.transcript_builder.build(
            video_id=clip_db.video_id,
            start_sec=clip_db.start_sec,
            end_sec=clip_db.end_sec
        )
        return Clip(
            clip_id=clip_id,
            video=video,
            transcript=transcript,
        )


class TranscriptArtifactBuilder:
    def build(self, video_id, start_sec=None, end_sec=None) -> Transcript:
        def calc_diff_time(start_vals, end_vals):
            diff_vals = start_vals[1:] - end_vals[:-1]
            return np.pad(diff_vals, (1, 0))

        def is_name(text):
            return re.search(r'君。?$', text)  # TODO: handle 参考人、大臣

        fp = Path(f'./out/transcript/{video_id}/data/transcript.csv')
        if not fp.exists():
            return Transcript()

        df = pd.read_csv(fp)
        df['diff_ms'] = calc_diff_time(df['start_ms'].values, df['end_ms'].values)
        df['has_gap'] = df['diff_ms'] > 0
        df['is_name'] = df['text'].apply(is_name)

        if start_sec:
            df = df[df['end_ms'] > start_sec * 1000]
        if end_sec:
            df = df[df['start_ms'] < end_sec * 1000]

        build_helper = TranscriptBuildHelper()
        for _, row in df.iterrows():
            word = Word(
                start=row['start_ms'] / 1000,
                end=row['end_ms'] / 1000,
                text=row['text']
            )
            if row['is_name']:
                build_helper.finish_utterance()  # not always correct when the moderator has multiple utterances
                build_helper.add_word(word)
                build_helper.finish_utterance()
            elif row['has_gap']:
                build_helper.finish_utterance()
                build_helper.add_word(word)
            else:
                build_helper.add_word(word)
        return build_helper.build()
