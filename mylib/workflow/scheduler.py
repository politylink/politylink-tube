from typing import List

from mylib.workflow.models import BaseOperator, StatusCode


class JobScheduler:
    def __init__(self, force_execute=False):
        self.force_execute = force_execute
        self.history = dict()

    def schedule(self, **kwargs) -> List[BaseOperator]:
        NotImplementedError

    def record(self, job: BaseOperator, status_code: StatusCode):
        self.history[job] = status_code

    def is_valid_job(self, job: BaseOperator):
        if job in self.history:
            return False
        if job.pre_execute(force_execute=self.force_execute) != StatusCode.SUCCESS:
            return False
        return True

    def filter_jobs(self, jobs: List[BaseOperator]) -> List[BaseOperator]:
        return list(filter(self.is_valid_job, jobs))

    def sort_jobs(self, jobs: List[BaseOperator]) -> List[BaseOperator]:
        return sorted(jobs, key=lambda x: x.context.priority, reverse=True)
