import re
from datetime import datetime


def format_date(dt: datetime):
    return dt.strftime('%Y年%m月%d日')


def format_duration(sec: float):
    sec = int(sec)
    hour = sec // 3600
    sec -= hour * 3600
    minute = sec // 60
    return f'{hour}h{minute}m'


def format_place(house: str, meeting: str):
    return f'{house} {meeting}'


SYMBOL_LEFT = '（(\[【'
SYMBOL_RIGHT = '\])）】'


def build_mask_phrase_pattern():
    phrases = [
        '拍手', '記者', '笑', '委員長', '字幕視聴ありがとうございました', '御静聴', '音声なし', '間', '司会', '質疑応答',
        '小声', '質問'
    ]
    pattern = r'[{0}]+\s*({1})\s*[{2}]+'.format(SYMBOL_LEFT, '|'.join(phrases), SYMBOL_RIGHT)
    return re.compile(pattern)


def build_remove_symbol_pattern():
    pattern = r'[{0}{1}]+'.format(SYMBOL_LEFT, SYMBOL_RIGHT)
    return re.compile(pattern)


def build_moderator_pattern():
    phrases = ['君', 'さん', '大臣', '参考人', '官', '長', '知事', '員']
    pattern = r'({0})。?$'.format('|'.join(phrases))
    return re.compile(pattern)


MASK_PHRASE_PATTERN = build_mask_phrase_pattern()
REMOVE_SYMBOL_PATTERN = build_remove_symbol_pattern()
MODERATOR_PATTERN = build_moderator_pattern()


def mask_phrase(text):
    return re.sub(MASK_PHRASE_PATTERN, '', text).strip()


def remove_symbol(text):
    return re.sub(REMOVE_SYMBOL_PATTERN, '', text).strip()


def clean_text(text):
    if is_moderator(text):
        # remarks from moderator are often wrapped by symbols, we can safely strip them all
        return remove_symbol(text)
    return mask_phrase(text)  # apply passive masking


def is_moderator(text):
    return re.search(MODERATOR_PATTERN, remove_symbol(text))
