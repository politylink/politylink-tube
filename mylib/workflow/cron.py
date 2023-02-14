from datetime import date
from pathlib import Path

from mylib.workflow.models import BashOperator


class ShugiinTvJob(BashOperator):
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start_date: date, end_date: date, log_fp: [str | Path], cache_enabled=False):
        start_date = start_date.strftime(self.DATE_FORMAT)
        end_date = end_date.strftime(self.DATE_FORMAT)
        bash_command = f'poetry run scrapy crawl shugiin_tv -a start_date={start_date} -a end_date={end_date} --set HTTPCACHE_ENABLED={cache_enabled}'
        super().__init__(bash_command=bash_command, log_fp=log_fp)


class SangiinTvJob(BashOperator):
    def __init__(self, start_id: int, log_fp: [str | Path], cache_enabled=False):
        bash_command = f'poetry run scrapy crawl sangiin_tv -a start_id={start_id} --set HTTPCACHE_ENABLED={cache_enabled}'
        super().__init__(bash_command=bash_command, log_fp=log_fp)
