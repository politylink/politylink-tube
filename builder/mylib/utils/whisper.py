import pandas as pd


def read_whisper_csv(fp):
    return pd.read_csv(fp, skipinitialspace=True, header=None, names=["start_ms", "end_ms", "text"])
