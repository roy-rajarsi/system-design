from typing import Any, Callable, Dict, Optional

from .active_email_service import ActiveEmailService
from .enums.task_scheduler_types import TaskSchedulerType
from .task import Task


class EmailServiceProxy:

    @staticmethod
    def send_email(sender_email_address: str, receiver_email_address: str, email_payload: Dict[str, Any], callback: Optional[Callable] = None) -> None:
        ActiveEmailService(task_scheduler_type=TaskSchedulerType.FIFO).schedule_email_dispatch(task=Task(sender_email_address=sender_email_address,
                                                                                                         receiver_email_address=receiver_email_address,
                                                                                                         email_payload=email_payload,
                                                                                                         callback=callback))
