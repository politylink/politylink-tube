import argparse
import logging
from pathlib import Path

import pandas as pd

from mylib.workflow.jobs import VADJob, WhisperJob, AudioSplitJob, MergeWhisperJob

LOGGER = logging.getLogger(__name__)


def main():
    audio_fp = Path(args.input)
    vad_fp = audio_fp.parent / 'vad.csv'
    transcript_fp = audio_fp.parent / 'transcript.csv'

    VADJob(audio_fp=audio_fp, out_fp=vad_fp).run()
    vad_df = pd.read_csv(vad_fp)

    result_fps = []
    for _, row in vad_df.iterrows():
        wav_fp = audio_fp.parent / '{}.wav'.format(row['id'])
        log_fp = audio_fp.parent / 'whisper_{}.log'.format(row['id'])
        result_fp = WhisperJob.get_result_fp(wav_fp)
        result_fps.append(result_fp)

        AudioSplitJob(audio_fp=audio_fp, start_sec=row['start_sec'], end_sec=row['end_sec'], out_fp=wav_fp).run()
        WhisperJob(wav_fp=wav_fp, log_fp=log_fp)

    MergeWhisperJob(vad_fp=vad_fp, result_fps=result_fps, out_fp=transcript_fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main()
