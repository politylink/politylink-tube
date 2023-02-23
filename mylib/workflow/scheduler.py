from typing import List

from mylib.workflow.models import BaseOperator, StatusCode


class JobScheduler:
    def __init__(self):
        self.failed_jobs = []

    def schedule(self, **kwargs) -> List[BaseOperator]:
        NotImplementedError

    def record_failed_job(self, job: BaseOperator):
        self.failed_jobs.append(job)

    def is_valid_job(self, job: BaseOperator):
        if job in self.failed_jobs:
            return False
        if job.pre_execute() != StatusCode.SUCCESS:
            return False
        return True

    def filter_jobs(self, jobs: List[BaseOperator]) -> List[BaseOperator]:
        return list(filter(self.is_valid_job, jobs))

    def sort_jobs(self, jobs: List[BaseOperator]) -> List[BaseOperator]:
        return sorted(jobs, key=lambda x: x.context.priority, reverse=True)
