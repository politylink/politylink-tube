from datetime import datetime

from mylib.utils import substrptime


def test_substrptime():
    text = '今日は2023年2月10日(日)です。'
    assert substrptime(text, '%Y年%m月%d日') == datetime(2023, 2, 10)
