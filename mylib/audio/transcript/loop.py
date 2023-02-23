import pandas as pd


class TranscriptLoopDetector:
    """
    Whisper sometimes falls into an infinite loop emitting the same sentence.
    """

    def detect(self, df, length_thresh=2, duration_sec_thresh=0):
        """
        :param df: transcript df
        :param length_thresh:
        :param duration_sec_thresh:
        :return: loop detection result
        """

        records = []
        record = {'text': '', 'start_ms': 0, 'end_ms': 0, 'len': 0}
        for _, row in df.iterrows():
            if row['text'] == record['text']:
                record['end_ms'] = row['end_ms']
                record['len'] += 1
            else:
                records.append(record)
                record = {'len': 1}
                record.update(row)
        records.append(record)

        out_df = pd.DataFrame(records)
        out_df = out_df[out_df['len'] >= length_thresh]
        out_df['start_sec'] = out_df['start_ms'] / 1000
        out_df['end_sec'] = out_df['end_ms'] / 1000
        out_df = out_df[(out_df['end_sec'] - out_df['start_sec']) >= duration_sec_thresh]

        out_df = out_df[['start_sec', 'end_sec', 'text']]

        return out_df
