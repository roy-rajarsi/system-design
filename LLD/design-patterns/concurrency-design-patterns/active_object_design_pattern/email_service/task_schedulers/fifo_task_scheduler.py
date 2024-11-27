from typing import List, override

from .task_scheduler import TaskScheduler
from email_service.enums.task_scheduler_types import TaskSchedulerType
from email_service.task import Task


class FifoTaskScheduler(TaskScheduler):

    def __init__(self) -> None:
        super().__init__()
        super().set_task_scheduler_type(task_scheduler_type=TaskSchedulerType.FIFO)
        self.__task_queue: List[Task] = list()

    @override
    def schedule_task(self, task: Task) -> None:
        with self.get_condition():
            self.__task_queue.append(task)
            self.get_condition().notify_all()

    @override
    def pop_task(self) -> Task:
        if self.is_empty():
            raise Exception('Pop Task called on Empty Task Scheduler')
        with self.get_condition():
            return self.__task_queue.pop(0)

    @override
    def is_empty(self) -> bool:
        is_empty: bool
        with self.get_condition():
            is_empty = len(self.__task_queue) == 0
        return is_empty
