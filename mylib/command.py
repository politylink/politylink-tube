import subprocess
from logging import getLogger
from typing import List

LOGGER = getLogger(__name__)


class CommandTask:
    def __init__(self, cmd: [str, List]):
        if isinstance(cmd, str):
            cmd = cmd.split()
        self.cmd = cmd

    def __repr__(self):
        return f'<$ {" ".join(self.cmd)}>'

    def run(self, wait=True, log_fp=None):
        LOGGER.info('run command: ' + ' '.join(self.cmd))
        log_fp = str(log_fp) or '/dev/null'
        with open(log_fp, 'w') as f:
            if wait:
                return subprocess.run(self.cmd, stdout=f, stderr=f, encoding='utf-8')
            else:
                return subprocess.Popen(self.cmd, stdout=f, stderr=f, encoding='utf-8')
