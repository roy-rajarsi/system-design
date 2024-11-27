from threading import Lock
from time import sleep
from typing import Any, Dict, Final, Optional


class EmailService:

    __email_service: Optional['EmailService'] = None
    __object_creation_lock: Final[Lock] = Lock()

    def __new__(cls, *args, **kwargs) -> 'EmailService':
        if cls.__email_service is None:
            with cls.__object_creation_lock:
                if cls.__email_service is None:
                    cls.__email_service = super().__new__(cls)
                    cls.__email_service.__init__()
        return cls.__email_service

    def __init__(self) -> None:
        self.__sender_email_address: Optional[str] = None
        self.__receiver_email_address: Optional[str] = None
        self.__email_payload: Dict[str, Any] = dict()

    def set_email_attributes(self, sender_email_address: str, receiver_email_address: str, email_payload: Dict[str, Any]) -> None:

        # set_email_attributes() is a Critical Section

        self.__sender_email_address: str = sender_email_address
        self.__receiver_email_address: str = receiver_email_address
        self.__email_payload: Dict[str, Any] = email_payload

    def send_email(self) -> None:

        # send_email() is a Critical Section

        print(f'Sending Email to {self.__receiver_email_address} from {self.__sender_email_address}...')
        print(f'Email Body: {self.__email_payload}')
        sleep(2)  # Time Consuming Process
        print('Email Sent')
