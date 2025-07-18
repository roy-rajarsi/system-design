from abc import ABC, abstractmethod
from typing import Any, Dict, Final

from mediator.mediator import Mediator


class Colleague(ABC):

    def __init__(self, colleague_id: str, mediator: Mediator) -> None:
        self.__colleague_id: Final[str] = colleague_id
        self.__mediator: Final[Mediator] = mediator

    def get_colleague_id(self) -> str:
        return self.__colleague_id

    def get_mediator(self) -> Mediator:
        return self.__mediator

    @abstractmethod
    def send_message(self, message: Dict[str, Any], receiver_colleague_id: str) -> None:
        pass

    @abstractmethod
    def receive_message_callback(self, message: Dict[str, Any], sender_colleague_id: str) -> None:
        pass
