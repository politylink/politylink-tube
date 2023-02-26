from typing import List

import numpy as np
import pandas as pd

from mylib.artifact.helpers import TranscriptBuildHelper
from mylib.artifact.models import Video, Clip, Transcript, Word, Annotation
from mylib.artifact.utils import format_date, format_duration, clean_text, is_moderator, format_time
from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Clip as ClipDb, Video as VideoDb, Annotation as AnnotationDb
from mylib.utils.path import PathHelper


class ClipArtifactBuilder:
    def __init__(self, sqlite_client: SqliteClient, path_helper: PathHelper):
        self.sqlite_client = sqlite_client
        self.transcript_builder = TranscriptArtifactBuilder(path_helper)

    def build(self, clip_id) -> Clip:
        clip_db: ClipDb = self.sqlite_client.select_first(ClipDb, id=clip_id)
        video_db: VideoDb = self.sqlite_client.select_first(VideoDb, id=clip_db.video_id)
        annotation_dbs: List[AnnotationDb] = self.sqlite_client.select_all(AnnotationDb, video_id=clip_db.video_id)

        video = Video(
            video_id=video_db.id,
            url=video_db.m3u8_url,
            page=video_db.page_url,
            start=clip_db.start_sec,
            end=clip_db.end_sec,
            date=format_date(video_db.datetime),
            duration=format_duration(clip_db.end_sec - clip_db.start_sec)
        )
        transcript = self.transcript_builder.build(
            video_id=clip_db.video_id,
            start_sec=clip_db.start_sec,
            end_sec=clip_db.end_sec
        )
        annotations = [convert_annotation(annotation_db) for annotation_db in annotation_dbs]

        return Clip(
            clip_id=clip_id,
            title=clip_db.title,
            video=video,
            transcript=transcript,
            annotations=annotations
        )


def convert_annotation(annotation_db: AnnotationDb) -> Annotation:
    text = annotation_db.speaker_name
    if annotation_db.speaker_info:
        text += f'（{annotation_db.speaker_info}）'

    return Annotation(
        start=annotation_db.start_sec,
        time=format_time(annotation_db.start_sec),
        text=text
    )


class TranscriptArtifactBuilder:
    def __init__(self, path_helper: PathHelper):
        self.path_helper = path_helper

    def build(self, video_id, start_sec=None, end_sec=None) -> Transcript:
        def calc_diff_time(start_vals, end_vals):
            diff_vals = start_vals[1:] - end_vals[:-1]
            return np.pad(diff_vals, (1, 0))

        fp = self.path_helper.get_transcript_fp(video_id)
        if not fp.exists():
            build_helper = TranscriptBuildHelper()
            build_helper.add_word(Word(
                start=start_sec,
                end=end_sec,
                text='（文字起こし作成中）'
            ))
            return build_helper.build()

        df = pd.read_csv(fp)
        df['text'] = df['text'].apply(clean_text)
        df = df[df['text'] != '']
        df['diff_ms'] = calc_diff_time(df['start_ms'].values, df['end_ms'].values)
        df['has_gap'] = df['diff_ms'] > 0
        df['is_moderator'] = df['text'].apply(is_moderator)

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
            if row['is_moderator']:
                build_helper.finish_utterance()  # not always correct when the moderator has multiple utterances
                build_helper.add_word(word)
                build_helper.finish_utterance()
            elif row['has_gap']:
                build_helper.finish_utterance()
                build_helper.add_word(word)
            else:
                build_helper.add_word(word)
        return build_helper.build()
