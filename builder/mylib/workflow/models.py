import subprocess
from dataclasses import dataclass, field
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


@dataclass
class OperatorContext:
    class_name: str = ""
    class_kwargs: Dict = field(default_factory=dict)
    in_fps: List[Path] = field(default_factory=list)
    out_fps: List[Path] = field(default_factory=list)
    log_fp: Path = None
    priority: int = 0


class BaseOperator:
    def __init__(self, context: OperatorContext):
        self.context = context

    def init_context(self, locals_: Dict) -> OperatorContext:
        """
        call this method at the top of the constructor
        """

        return OperatorContext(
            class_name=self.__class__.__name__,
            class_kwargs={k: v for k, v in locals_.items() if k not in ["self", "__class__"]},
        )

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
        if self.context.in_fps:
            is_input_ready = all([Path(fp).exists() for fp in self.context.in_fps])
            if not is_input_ready:
                return StatusCode.NOT_READY

        if self.context.out_fps:
            is_output_ready = all([Path(fp).exists() for fp in self.context.out_fps])
            if is_output_ready and not force_execute:
                return StatusCode.SKIP

        return StatusCode.SUCCESS

    def post_execute(self) -> StatusCode:
        return StatusCode.SUCCESS

    def execute(self, **kwargs) -> StatusCode:
        raise NotImplementedError()


class BashOperator(BaseOperator):
    def __init__(self, bash_command: str, cwd=".", **kwargs):
        super().__init__(**kwargs)
        self.bash_command = bash_command
        self.cwd = cwd

    def __repr__(self):
        return f"<$ {self.bash_command}>"

    def __eq__(self, other):
        if isinstance(other, BashOperator):
            return self.bash_command == other.bash_command
        return False

    def __hash__(self):
        return hash(self.bash_command)

    def execute(self, **kwargs):
        log_fp = self.context.log_fp or "/dev/null"
        with open(log_fp, "w") as f:
            subprocess.run(self.bash_command.split(), cwd=self.cwd, stdout=f, stderr=f, encoding="utf-8")
        return StatusCode.SUCCESS  # TODO: check run result


class PythonOperator(BaseOperator):
    def __init__(self, python_callable, **kwargs):
        super().__init__(**kwargs)
        self.python_callable = python_callable

    def __repr__(self):
        arg_str = ",".join(
            ["{}={}".format(k, self.context.class_kwargs[k]) for k in sorted(self.context.class_kwargs.keys())]
        )
        return f"<{self.context.class_name}({arg_str})>"

    def __eq__(self, other):
        if isinstance(other, PythonOperator):
            return (self.context.class_name == other.context.class_name) and (
                self.context.class_kwargs == other.context.class_kwargs
            )
        return False

    def __hash__(self):
        return hash(self.__repr__())

    def execute(self, **kwargs):
        try:
            self.python_callable()
        except Exception:
            LOGGER.exception(f"failed to execute python callable")
            return StatusCode.FAILURE
        return StatusCode.SUCCESS
