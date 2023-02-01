import argparse
import logging
import os
import re
from pathlib import Path

import requests

from mylib.command import CommandTask
from mylib.ffmpeg import read_silence_df, to_segment_df

LOGGER = logging.getLogger(__name__)


def get_m3u8_url(video_url):
    try:
        response = requests.get(video_url)
        pattern = 'https?://.*playlist.m3u8'
        mm3u8_url = re.search(pattern, response.text).group()
        return mm3u8_url.replace('http://', 'https://')
    except Exception:
        raise ValueError(f'failed to extract m3u8 url from {video_url}')


def build_download_task(m3u8_url, audio_fp):
    cmd = f'ffmpeg -i {m3u8_url} {audio_fp}'
    return CommandTask(cmd=cmd, out_fp=audio_fp)


def build_silence_task(audio_fp, out_fp):
    cmd = f'ffmpeg -i {audio_fp} -af silencedetect=d=10:n=-10dB,ametadata=mode=print:file={out_fp} -f null -'
    return CommandTask(cmd=cmd, out_fp=out_fp)


def build_split_task(audio_fp, start, end, out_fp):
    duration = end - start
    cmd = f'ffmpeg -y -ss {start} -i {audio_fp} -t {duration} -ar 16000 -ac 1 -c:a pcm_s16le {out_fp}'
    return CommandTask(cmd=cmd, out_fp=out_fp)


def build_transcribe_task(wav_fp, model='small'):
    whisper_dir = Path(os.environ['WHISPER_ROOT'])
    bin_fp = whisper_dir / 'main'
    model_fp = whisper_dir / f'models/ggml-{model}.bin'
    out_fp = wav_fp.parent / (wav_fp.name + '.csv')
    cmd = f'{bin_fp} --model {model_fp} --language ja --file {wav_fp} --output-csv'
    return CommandTask(cmd=cmd, out_fp=out_fp)


def main():
    log_dir = Path(args.output) / str(args.job) / 'log'
    data_dir = Path(args.output) / str(args.job) / 'data'

    log_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    m3u8_url = get_m3u8_url(args.input)
    mp3_fp = data_dir / 'audio.mp3'
    log_fp = log_dir / 'download.log'
    silence_fp = data_dir / 'silence.txt'
    segment_fp = data_dir / 'segment.csv'

    build_download_task(m3u8_url, mp3_fp).run(log_fp=log_fp)
    build_silence_task(mp3_fp, silence_fp).run()
    silence_df = read_silence_df(silence_fp)
    segment_df = to_segment_df(silence_df)
    segment_df.to_csv(segment_fp, index=False)
    LOGGER.info(f'found {len(segment_df)} segments')

    for _, row in segment_df.iterrows():
        wav_fp = data_dir / '{}.wav'.format(row['segment_id'])
        log_fp = log_dir / '{}.log'.format(row['segment_id'])
        build_split_task(mp3_fp, row['start'], row['end'], wav_fp).run()
        build_transcribe_task(wav_fp, model=args.model).run(log_fp=log_fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='審議中継のURLから文字起こしを生成する')
    parser.add_argument('-i', '--input', help='動画URL', required=True)
    parser.add_argument('-j', '--job', help='ジョブID', type=int, required=True)
    parser.add_argument('-o', '--output', help='出力ディレクトリ', default='./out/transcript')
    parser.add_argument('-m', '--model', help='Whisperのモデル', default='small')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
