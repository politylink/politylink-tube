import librosa
import numpy as np
import pandas as pd


class AudioModel:
    def __init__(self, fp, frame_sec=0.02, hop_sec=0.02):
        """
        :param fp: audio file path
        :param frame_sec: RMS window size in second. The larger, the slower.
        :param hop_sec: RMS window offset in second. The larger, the faster.
        """

        self.y, self.sample_rate = librosa.load(fp, sr=None)
        self.frame_length = int(self.sample_rate * frame_sec)
        self.hop_length = int(self.sample_rate * hop_sec)
        self.rms = librosa.feature.rms(y=self.y, frame_length=self.frame_length, hop_length=self.hop_length)[0]
        self.db = librosa.amplitude_to_db(self.rms)

    def get_audio(self, start_sec, end_sec):
        """
        get audio subset by second
        """

        start = start_sec * self.sample_rate
        end = end_sec * self.sample_rate
        return self.y[start:end]


class VoiceActivityDetector:
    """
    simple voice activity detector based on sound volume
    """

    def detect(self, audio: AudioModel, db_thresh=-25, agg_thresh=0.02, window_sec=5, silence_sec=30):
        """
        :param audio: audio model
        :param db_thresh: threshold for DB binarization
        :param agg_thresh: threshold for ratio of positive samples in aggregation window
        :param window_sec: aggregation window size in second
        :param silence_sec: ignore silence shorter than this threshold
        :return: detection result as DataFrame
        """

        db_bin = audio.db >= db_thresh
        window_length = int(audio.sample_rate / audio.hop_length * window_sec)  # # of samples to calculate stats
        pad_length = (window_length - (len(audio.db) % window_length)) % window_length
        db_bin = np.pad(db_bin, (0, pad_length))
        assert db_bin.size % window_length == 0
        db_agg = db_bin.reshape(-1, window_length).mean(axis=1)  # ratio of active samples in each window

        db_agg_bin = db_agg >= agg_thresh
        db_agg_bin = fill_gap(db_agg_bin, int(silence_sec / window_sec / 2))
        db_agg_bin_ws = np.concatenate(([False], db_agg_bin, [False]))  # add sentinel for interval calculation
        interval_mat = np.flatnonzero(np.diff(db_agg_bin_ws.astype(int))).reshape((-1, 2))

        out_df = pd.DataFrame(interval_mat, columns=['start_frame', 'end_frame'])
        out_df['is_test_noise'] = out_df.apply(
            lambda x: self.is_test_noise(db_agg[x['start_frame']:x['end_frame']]), axis=1)
        out_df = out_df[~out_df['is_test_noise']]

        out_df['id'] = range(1, len(out_df) + 1)
        out_df['start_sec'] = out_df['start_frame'] * window_sec
        out_df['end_sec'] = out_df['end_frame'] * window_sec
        out_df = out_df[['id', 'start_sec', 'end_sec']]

        return out_df

    @staticmethod
    def is_test_noise(db_agg, sample_ratio_thresh=0.75, db_ratio_thresh=0.95):
        """
        detect test noise

        :param db_agg:
        :param sample_ratio_thresh:
        :param db_ratio_thresh:
        :return:
        """

        if len(db_agg) < 4:  # not enough samples
            return False
        sample_count = db_agg.size
        high_count = (db_agg >= db_ratio_thresh).sum()
        return (high_count / sample_count) >= sample_ratio_thresh


def fill_gap(a, k):
    """
    fill gap maximum size of 2k
    """

    if k == 0:
        return a

    v = np.ones(2 * k + 1)
    a = np.convolve(a, v) > 0  # dilation
    a = np.convolve(a, v) == v.size  # erosion
    return a[2 * k:-2 * k]
