import argparse
import logging
import re
from pathlib import Path

import pandas as pd
import requests

from mylib.command import CommandTask

LOGGER = logging.getLogger(__name__)


def get_m3u8_url(video_url):
    try:
        response = requests.get(video_url)
        pattern = 'https?://.*playlist.m3u8'
        mm3u8_url = re.search(pattern, response.text).group()
        return mm3u8_url.replace('http://', 'https://')
    except Exception:
        raise ValueError(f'failed to extract m3u8 url from {video_url}')


def read_silence_df(silence_fp):
    """
    parse silence detection result by FFmpeg
    return (start, end) of detected silence
    """

    with open(silence_fp, 'r') as f:
        lines = f.readlines()

    records = []
    start = None
    pattern = r'silence_(start|end): ([0-9.]+)'
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
    silence_df = pd.DataFrame(records)
    return silence_df


def to_segment_df(silence_df):
    """
    inverse silence_df to
    """

    start = 0
    records = []
    for _, row in silence_df.iterrows():
        if row['start'] > 0:
            records.append({
                'segment_id': len(records),
                'start': int(start),
                'end': int(row['start']) + 1
            })
        start = row['end']
    segment_df = pd.DataFrame(records)
    return segment_df


def build_download_task(m3u8_url, mp3_fp, log_fp):
    cmd = f'ffmpeg -i {m3u8_url} {mp3_fp}'
    task = CommandTask(cmd, log_fp)
    return task


def build_silence_task(audio_fp, out_fp):
    cmd = f'ffmpeg -i {audio_fp} -af silencedetect=d=10 -f null -'
    task = CommandTask(cmd, out_fp)
    return task


def build_split_task(audio_fp, start, end, out_fp):
    duration = end - start
    cmd = f'ffmpeg -y -ss {start} -i {audio_fp} -t {duration} -ar 16000 -ac 1 -c:a pcm_s16le {out_fp}'
    task = CommandTask(cmd)
    return task


def build_transcribe_task(wav_fp):
    whisper_direc = '/Users/mitsuki/sandbox/whisper.cpp'
    bin_fp = f'{whisper_direc}/main'
    model_fp = f'{whisper_direc}/models/ggml-small.bin'
    cmd = f'{bin_fp} --model {model_fp} --language ja --file {wav_fp} --output-csv'
    task = CommandTask(cmd)
    return task


def main():
    m3u8_url = get_m3u8_url(args.input)

    log_dir = Path(args.output) / str(args.job) / 'log'
    audio_dir = Path(args.output) / str(args.job) / 'audio'
    log_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    full_fp = audio_dir / 'full.mp3'
    silence_fp = audio_dir / 'silence.csv'

    build_download_task(m3u8_url, full_fp, log_dir / 'download.log').run()
    build_silence_task(full_fp, silence_fp).run()

    silence_df = read_silence_df(silence_fp)
    segment_df = to_segment_df(silence_df)
    LOGGER.info(f'found {len(segment_df)} segments')
    segment_fp = audio_dir / 'segment.csv'
    segment_df.to_csv(segment_fp, index=False)

    for _, row in segment_df.iterrows():
        seg_fp = audio_dir / '{}.wav'.format(row['segment_id'])
        build_split_task(full_fp, row['start'], row['end'] - row['start'], seg_fp).run()
        build_transcribe_task(seg_fp).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='審議中継のURLから文字起こしを生成する')
    parser.add_argument('-i', '--input', help='動画URL', required=True)
    parser.add_argument('-j', '--job', help='ジョブID', type=int, required=True)
    parser.add_argument('-o', '--output', help='出力ディレクトリ', default='./out/transcript')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
