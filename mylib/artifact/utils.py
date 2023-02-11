import re
from typing import List

import numpy as np
import pandas as pd

from mylib.artifact.builders import TranscriptBuilder
from mylib.artifact.models import Transcript, Word


def build_transcript_from_whisper(whisper_fp, offset_sec=0):
    def calc_diff_time(start_vals, end_vals):
        diff_vals = start_vals[1:] - end_vals[:-1]
        return np.pad(diff_vals, (1, 0))

    def is_name(text):
        return re.search(r'君。?$', text)

    df = pd.read_csv(whisper_fp, skipinitialspace=True, header=None, names=['start_ms', 'end_ms', 'text'])
    df['diff_ms'] = calc_diff_time(df['start_ms'].values, df['end_ms'].values)
    df['has_gap'] = df['diff_ms'] > 0
    df['is_name'] = df['text'].apply(is_name)

    builder = TranscriptBuilder()
    for _, row in df.iterrows():
        word = Word(
            start=row['start_ms'] / 1000 + offset_sec,
            end=row['end_ms'] / 1000 + offset_sec,
            text=row['text']
        )
        if row['is_name']:
            builder.finish_utterance()  # not always correct when the moderator has multiple utterances
            builder.add_word(word)
            builder.finish_utterance()
        elif row['has_gap']:
            builder.finish_utterance()
            builder.add_word(word)
        else:
            builder.add_word(word)

    return builder.build()


def merge_transcripts(transcripts: List[Transcript]):
    utterances = []
    for transcript in transcripts:
        utterances += transcript.utterances
    utterances = sorted(utterances, key=lambda x: x.start)
    return Transcript(utterances=utterances)
