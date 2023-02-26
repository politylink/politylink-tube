from datetime import datetime

from mylib.artifact.utils import format_date, format_duration, clean_text, is_moderator, format_time


def test_format_date():
    assert format_date(datetime(2023, 2, 1)) == '2023年02月01日(水)'


def test_format_duration():
    assert format_duration(30.5) == '0h0m'
    assert format_duration(90.0) == '0h1m'
    assert format_duration(7200.3) == '2h0m'


def test_format_time():
    assert format_time(0) == '0:00'
    assert format_time(30.5) == '0:30'
    assert format_time(90.0) == '1:30'
    assert format_time(1200.0) == '20:00'
    assert format_time(7200.3) == '2:00:00'


def test_clean_text():
    assert clean_text('(笑)') == ''
    assert clean_text(' (  笑 ) ') == ''
    assert clean_text('(音声なし)') == ''
    assert clean_text('音声なし') == '音声なし'
    assert clean_text('（拍手）こんにちは（笑）') == 'こんにちは'
    assert clean_text('（太郎君）') == '太郎君'


def test_is_moderator():
    assert is_moderator('太郎君')
    assert not is_moderator('太郎君ですか')
    assert is_moderator('(( 太郎君 )) ')


def test_is_moderator_positive():
    phrases = ['君', 'さん', '大臣', '参考人', '審議官', '政務官', '局長', '次長', '部長', '知事', '議長', '調整官', '官房長官',
               '委員', '議員']
    for phrase in phrases:
        assert is_moderator(phrase)
