import subprocess
from enum import IntEnum
from logging import getLogger
from pathlib import Path
from typing import List, Dict

LOGGER = getLogger(__name__)


class StatusCode(IntEnum):
    FAILURE = 0
    SUCCESS = 1
    SKIP = 2
    NOT_READY = 3


# TODO: define OperatorContext to store in/out/log files, original command arguments...

class BaseOperator:
    def __init__(self, *,
                 in_fps: List[Path] = None,
                 out_fps: List[Path] = None,
                 log_fp: [str | Path] = None,
                 priority: int = 0):

        self.in_fps = in_fps or []
        self.out_fps = out_fps or []
        self.log_fp = log_fp
        self.priority = priority

    def run(self, force_execute=False, **kwargs) -> StatusCode:
        pre_execute_result = self.pre_execute(force_execute)
        if pre_execute_result != StatusCode.SUCCESS:
            return pre_execute_result

        execute_result = self.execute(**kwargs)
        if execute_result != StatusCode.SUCCESS:
            return execute_result

        post_execute_result = self.post_execute()
        if post_execute_result != StatusCode.SUCCESS:
            return post_execute_result

        return StatusCode.SUCCESS

    def pre_execute(self, force_execute=False) -> StatusCode:
        if self.in_fps:
            is_input_ready = all([Path(fp).exists() for fp in self.in_fps])
            if not is_input_ready:
                return StatusCode.NOT_READY

        if self.out_fps:
            is_output_ready = all([Path(fp).exists() for fp in self.out_fps])
            if is_output_ready and not force_execute:
                return StatusCode.SKIP

        return StatusCode.SUCCESS

    def post_execute(self) -> StatusCode:
        return StatusCode.SUCCESS

    def execute(self, **kwargs) -> StatusCode:
        raise NotImplementedError()


class BashOperator(BaseOperator):
    def __init__(self, bash_command: str, **kwargs):
        super().__init__(**kwargs)
        self.bash_command = bash_command

    def __repr__(self):
        return f'<$ {self.bash_command}>'

    def __eq__(self, other):
        if isinstance(other, BashOperator):
            return self.bash_command == other.bash_command
        return False

    def execute(self, **kwargs):
        log_fp = self.log_fp or '/dev/null'
        with open(log_fp, 'w') as f:
            subprocess.run(self.bash_command.split(), stdout=f, stderr=f, encoding='utf-8')
        return StatusCode.SUCCESS  # TODO: check run result


class PythonOperator(BaseOperator):
    def __init__(self, python_callable, context: Dict, **kwargs):
        super().__init__(**kwargs)
        self.context = context
        self.python_callable = python_callable

    def __repr__(self):
        return f'<{self.context["class"]}({self.context["args"]})>'

    def __eq__(self, other):
        if isinstance(other, PythonOperator):
            return self.context == other.context
        return False

    def execute(self, **kwargs):
        try:
            self.python_callable()
        except Exception:
            LOGGER.exception(f'failed to execute python callable')
            return StatusCode.FAILURE
        return StatusCode.SUCCESS
