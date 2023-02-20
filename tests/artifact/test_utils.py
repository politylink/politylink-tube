from datetime import datetime

from mylib.artifact.utils import format_date, format_duration


def test_format_date():
    assert format_date(datetime(2023, 2, 1)) == '2023年02月01日'


def test_fromat_duration():
    assert format_duration(30.5) == '0h0m'
    assert format_duration(90.0) == '0h1m'
    assert format_duration(7200.3) == '2h0m'
