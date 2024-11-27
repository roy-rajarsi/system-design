from threading import Lock, Thread
from typing import Final, Optional

from .email_service import EmailService
from .task import Task
from .enums.task_scheduler_types import TaskSchedulerType
from .task_schedulers.task_scheduler import TaskScheduler
from .factories.task_scheduler_factory import TaskSchedulerFactory


class ActiveEmailService:

    __active_email_service: Optional['ActiveEmailService'] = None
    __object_creation_lock: Final[Lock] = Lock()
    __params_initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'ActiveEmailService':
        if cls.__active_email_service is None:
            with cls.__object_creation_lock:
                if cls.__active_email_service is None:
                    cls.__active_email_service = super().__new__(cls)
                    cls.__active_email_service.__init__(*args, **kwargs)
        return cls.__active_email_service

    def __init__(self, *args, **kwargs) -> None:
        if not self.__class__.__params_initialized:
            task_scheduler_type: TaskSchedulerType = args[0] if len(args) > 0 else kwargs.get('task_scheduler_type')
            self.__task_scheduler: TaskScheduler = TaskSchedulerFactory.get_task_scheduler(task_scheduler_type=task_scheduler_type)()
            self.__worker: Thread = Thread(name='EmailDispatcher', target=self.__dispatch_email)
            self.__email_service: EmailService = EmailService()
            self.__email_service_lock: Lock = Lock()
            self.__worker.start()
            self.__class__.__params_initialized = True

    def schedule_email_dispatch(self, task: Task) -> None:
        with self.__task_scheduler.get_condition():
            self.__task_scheduler.schedule_task(task=task)

    def __dispatch_email(self) -> None:
        while True:
            with self.__task_scheduler.get_condition():
                if self.__task_scheduler.is_empty():
                    self.__task_scheduler.get_condition().wait()

            with self.__task_scheduler.get_condition():
                task: Task = self.__task_scheduler.pop_task()

            with self.__email_service_lock:
                self.__email_service.set_email_attributes(sender_email_address=task.get_sender_email_address(),
                                                          receiver_email_address=task.get_receiver_email_address(),
                                                          email_payload=task.get_email_payload())
                self.__email_service.send_email()
                print('Running Callback after sending email')
                task.get_callbacK()()

