from mylib.artifact.models import Word, Utterance, Transcript


class TranscriptBuilder:
    def __init__(self):
        self.utterances = [Utterance()]

    def add_word(self, word: Word):
        self.utterances[-1].words.append(word)

    def finish_utterance(self):
        latest = self.utterances[-1]
        if not latest.words:
            return
        latest.start = latest.words[0].start
        latest.end = latest.words[-1].end
        self.utterances.append(Utterance())

    def build(self):
        self.finish_utterance()
        assert len(self.utterances[-1].words) == 0
        self.utterances.pop()
        return Transcript(utterances=self.utterances)
