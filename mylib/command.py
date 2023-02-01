import subprocess
from logging import getLogger
from typing import List

LOGGER = getLogger(__name__)


class CommandTask:
    def __init__(self, cmd: [str, List], out_fp=None):
        if isinstance(cmd, str):
            cmd = cmd.split()
        self.cmd = cmd
        self.out_fp = str(out_fp) if out_fp else '/dev/null'

    def __repr__(self):
        return f'<$ {" ".join(self.cmd)}>'

    def run(self, wait=True):
        LOGGER.info('run command: ' + ' '.join(self.cmd))
        with open(self.out_fp, 'w') as f:
            if wait:
                return subprocess.run(self.cmd, stdout=f, stderr=f, encoding='utf-8')
            else:
                return subprocess.Popen(self.cmd, stdout=f, stderr=f, encoding='utf-8')
