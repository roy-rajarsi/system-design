from typing import Type

from email_service.enums.task_scheduler_types import TaskSchedulerType
from email_service.task_schedulers.task_scheduler import TaskScheduler
from email_service.task_schedulers.fifo_task_scheduler import FifoTaskScheduler


class TaskSchedulerFactory:

    @staticmethod
    def get_task_scheduler(task_scheduler_type: TaskSchedulerType) -> Type['TaskScheduler']:
        if task_scheduler_type is TaskSchedulerType.FIFO:
            return FifoTaskScheduler
