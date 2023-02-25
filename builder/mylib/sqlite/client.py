from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mylib.sqlite.schema import Base
from mylib.utils.path import PathHelper


class SqliteClient:
    def __init__(self, url=None, host=None, echo=False):
        if not url:
            url = PathHelper(host).get_sqlite_url()
        engine = create_engine(url, echo=echo)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        try:
            self.close()
        except:  # HOTFIX: session may be already closed?
            pass

    def close(self):
        self.session.close()

    def insert(self, instance) -> bool:
        self.session.add(instance)
        self.session.commit()
        return True

    def insert_all(self, instances) -> bool:
        self.session.add_all(instances)
        self.session.commit()
        return True

    def delete(self, instance) -> bool:
        self.session.delete(instance)
        self.session.commit()
        return True

    def upsert(self, instance, keys) -> bool:
        if not keys:
            raise ValueError('select at least one merge key')

        kwargs = dict([(key, getattr(instance, key)) for key in keys])
        db_instance = self.select_first(instance.__class__, **kwargs)
        if not db_instance:
            return self.insert(instance)

        for col in instance.__table__.columns:
            val = getattr(instance, col.name)
            if val is not None and not col.primary_key:
                setattr(db_instance, col.name, val)
        self.session.commit()
        return True

    def exists(self, class_, **kwargs):
        return self.select_first(class_, **kwargs) is not None

    def select_first(self, class_, **kwargs):
        return self.session.query(class_).filter_by(**kwargs).first()

    def select_all(self, class_, **kwargs) -> List:
        return self.session.query(class_).filter_by(**kwargs).all()

    def commit(self):
        return self.session.commit()
