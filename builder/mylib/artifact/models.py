from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Video(BaseModel):
    url: str = ''
    page: str = ''
    start: float = 0.
    end: float = 0.
    date: str = ''
    duration: str = ''
    place: str = ''
    speaker: str = ''


class Word(BaseModel):
    start: float = 0.
    end: float = 0.
    text: str = ''

    def __len__(self):
        return len(self.text)


class Utterance(BaseModel):
    start: float = 0.
    end: float = 0.
    words: List[Word] = Field(default_factory=list)

    def __len__(self):
        return len(self.words)


class Transcript(BaseModel):
    utterances: List[Utterance] = Field(default_factory=list)

    def __len__(self):
        return len(self.utterances)


class Clip(BaseModel):
    clip_id: int = Field(0, alias='clipId')
    title: str = ''
    video: Video = Field(default_factory=Video)
    transcript: Transcript = Field(default_factory=Transcript)

    class Config:
        allow_population_by_field_name = True
