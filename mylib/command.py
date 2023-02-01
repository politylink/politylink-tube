import subprocess
from logging import getLogger
from typing import List

LOGGER = getLogger(__name__)


class CommandTask:
    def __init__(self, cmd: [str, List], out_fp):
        if isinstance(cmd, str):
            cmd = cmd.split()
        self.cmd = cmd
        self.out_fp = out_fp

    def __repr__(self):
        return f'<$ {" ".join(self.cmd)}>'

    def run(self, wait=True, force=False, log_fp=None):
        if self.out_fp.exists() and not force:
            LOGGER.info('skip command: ' + ' '.join(self.cmd))
            return

        LOGGER.info('run command: ' + ' '.join(self.cmd))
        log_fp = str(log_fp) or '/dev/null'
        with open(log_fp, 'w') as f:
            if wait:
                return subprocess.run(self.cmd, stdout=f, stderr=f, encoding='utf-8')
            else:
                return subprocess.Popen(self.cmd, stdout=f, stderr=f, encoding='utf-8')
