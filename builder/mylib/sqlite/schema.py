from sqlalchemy import Column, Integer, String, DateTime, Float, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Serializable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def serialize(self, keys=None):
        keys = keys or [col.name for col in self.__table__.columns]
        d = dict()
        for k in keys:
            v = getattr(self, k)
            if v is not None:
                d[k] = v
        return d

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.serialize()}>"


class Video(Base, Serializable):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    m3u8_url = Column(String, index=True)  # order matters when importing CSV with db/init.sql
    page_url = Column(String)
    datetime = Column(DateTime)
    house_name = Column(String)
    meeting_name = Column(String)


class Annotation(Base, Serializable):
    __tablename__ = "annotation"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, index=True)
    start_sec = Column(Float)
    end_sec = Column(Float)
    speaker_name = Column(String)
    speaker_info = Column(String)
    producer = Column(String)


class ClipType:
    UNKNOWN = 0
    FULL = 1
    SPEAKER = 2
    TOPIC = 3


class Clip(Base, Serializable):
    __tablename__ = "clip"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    video_id = Column(Integer, index=True)
    start_sec = Column(Float)
    end_sec = Column(Float)
    title = Column(String)
    type = Column(Integer)


Index(
    "ix_annotation_videoId_startSec_producer",
    Annotation.__table__.c.video_id,
    Annotation.__table__.c.start_sec,
    Annotation.__table__.c.producer,
)
