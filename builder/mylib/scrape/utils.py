import re
from datetime import datetime


def extract_text(selector, separator=" ", direct_only=False):
    text_xpath = "./text()" if direct_only else ".//text()"
    texts = selector.xpath(text_xpath).getall()
    return separator.join([text.strip() for text in texts]).strip()


def extract_href(selector):
    return selector.xpath(".//@href").get()


def to_datetime(dt_str):
    pattern = r"(\d+)年(\d+)月(\d+)日"
    m = re.search(pattern, dt_str)
    if not m:
        raise ValueError(f"{dt_str} does not match with {pattern}")
    return datetime.strptime(m.group(), "%Y年%m月%d日")


def scrape_dl(selector, scrape_url=False) -> dict:
    d = dict()
    for dt, dd in zip(selector.xpath(".//dt"), selector.xpath(".//dd")):
        k, v = scrape_kv(dt, dd, scrape_url)
        if k not in d:
            d[k] = v
    return d


def scrape_table(selector, scrape_url=False) -> dict:
    d = dict()
    for tr in selector.xpath(".//tr"):
        k, v = scrape_kv(tr.xpath(".//th"), tr.xpath(".//td"), scrape_url)
        if k not in d:
            d[k] = v
    return d


def scrape_kv(key_selector, val_selector, scrape_url=False):
    """
    key: lower case text
    val: text or URL
    """

    key = extract_text(key_selector).strip().lower()
    if scrape_url and val_selector.xpath(".//a"):
        val = extract_href(val_selector)
    else:
        val = extract_text(val_selector)
    return key, val
