import re

import pandas as pd


def read_silence_df(silence_fp):
    """
    parse silence detection result by FFmpeg
    return (start, end) of detected silence intervals
    """

    with open(silence_fp, 'r') as f:
        lines = f.readlines()

    records = []
    start = None
    pattern = r'silence_(start|end)=([0-9.]+)'
    for line in lines:
        match = re.search(pattern, line)
        if match:
            is_start = match.group(1) == 'start'
            time = float(match.group(2))
            if is_start:
                start = time
            else:
                records.append({'start': start, 'end': time})
                start = None
    if start is not None:
        records.append({'start': start, 'end': None})
    silence_df = pd.DataFrame(records)
    return silence_df


def to_segment_df(silence_df):
    """
    inverse silence intervals to get audio intervals
    """

    start = 0
    records = []
    for _, row in silence_df.iterrows():
        if row['start'] > 0:
            records.append({
                'start': int(start),
                'end': int(row['start']) + 1
            })
        start = row['end']
    # TODO: handle the last audio interval (in case no silence detected at the end)
    segment_df = pd.DataFrame(records)
    segment_df['duration'] = segment_df['end'] - segment_df['start']
    segment_df = segment_df[segment_df['duration'] >= 5]
    segment_df['segment_id'] = range(len(segment_df))
    return segment_df
