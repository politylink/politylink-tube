from datetime import datetime


def format_date(dt: datetime):
    # can not use strftime as it include 0 padding
    return '{}年{}月{}日'.format(dt.year, dt.month, dt.day)


def format_duration(sec: float):
    hour = sec // 3600
    sec -= hour * 3600
    minute = sec // 60
    return f'{hour}h{minute}m'


def format_place(house: str, meeting: str):
    return f'{house} {meeting}'
