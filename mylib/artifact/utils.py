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
