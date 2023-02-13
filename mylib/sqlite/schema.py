from sqlalchemy import Column, Integer, String, DateTime
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
        return f'<{self.__class__.__name__} {self.serialize()}>'


class Video(Base, Serializable):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    url = Column(String, index=True)
    datetime = Column(DateTime)
    meeting_name = Column(String)


class Clip(Base, Serializable):
    __tablename__ = 'clip'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer)
    speaker_name = Column(String)
