from datetime import datetime
from pathlib import Path

import pytest

from mylib.sqlite.client import SqliteClient
from mylib.sqlite.schema import Video


class TestSqliteClient:

    @pytest.fixture
    def client(self):
        Path('./test.db').unlink(missing_ok=True)
        yield SqliteClient('sqlite:///test.db')
        Path('./test.db').unlink(missing_ok=True)

    def test_insert(self, client):
        client.insert(Video(url='1'))
        assert len(client.select_all(Video)) == 1
        client.insert(Video(url='2'))
        assert len(client.select_all(Video)) == 2
        client.insert(Video(url='1'))
        assert len(client.select_all(Video)) == 3
        assert len(client.select_all(Video, url='1')) == 2

    def test_merge(self, client):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        client.merge(Video(id=1, url='1'), keys=['url'])
        assert len(client.select_all(Video)) == 1
        client.merge(Video(id=2, url='1', datetime=dt), keys=['url'])
        assert len(client.select_all(Video)) == 1

        db_instance = client.select_first(Video, url='1')
        assert db_instance.id == 1
        assert db_instance.datetime == dt

    def test_merge_fail_with_empty_keys(self, client):
        with pytest.raises(ValueError):
            client.merge(Video(id=1, url='1'), keys=[])
