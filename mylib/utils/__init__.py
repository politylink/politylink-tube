import re
from datetime import datetime


def substrptime(date_str, date_format) -> datetime:
    """
    apply strptime to substr
    """

    pattern = re.sub(r'%[a-zA-Z]+', '\\\d+', date_format)
    match = re.search(pattern, date_str)
    if not match:
        raise ValueError(f'{date_str} does not contain {date_format}')
    return datetime.strptime(match.group(), date_format)
