from abc import ABC, abstractmethod
from threading import Condition
from typing import Final, Optional

from email_service.enums.task_scheduler_types import TaskSchedulerType
from email_service.task import Task


class TaskScheduler(ABC):

    def __init__(self) -> None:
        self.__task_scheduler_type: Optional[TaskSchedulerType] = None
        self.__condition: Final[Condition] = Condition()

    def set_task_scheduler_type(self, task_scheduler_type: TaskSchedulerType) -> None:
        self.__task_scheduler_type = task_scheduler_type

    def get_condition(self) -> Condition:
        return self.__condition

    @abstractmethod
    def schedule_task(self, task: Task) -> None:
        pass

    @abstractmethod
    def pop_task(self) -> Task:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass
