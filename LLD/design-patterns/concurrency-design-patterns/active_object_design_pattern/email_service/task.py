from typing import Any, Callable, Dict, Final, Optional


class Task:

    def __init__(self, sender_email_address: str, receiver_email_address: str, email_payload: Dict[str, Any], callback: Optional[Callable] = None) -> None:
        self.__sender_email_address: Final[str] = sender_email_address
        self.__receiver_email_address: Final[str] = receiver_email_address
        self.__email_payload: Final[Dict[str, Any]] = email_payload
        self.__callback: Final[Callable] = callback

    def get_sender_email_address(self) -> str:
        return self.__sender_email_address

    def get_receiver_email_address(self) -> str:
        return self.__receiver_email_address

    def get_email_payload(self) -> Dict[str, Any]:
        return self.__email_payload

    def get_callbacK(self) -> Optional[Callable]:
        return self.__callback
