import librosa


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
