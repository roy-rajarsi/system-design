from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING, Final, Set

if TYPE_CHECKING:
    from colleague.colleague import Colleague


class Mediator(ABC):

    def __init__(self, mediator_id: str) -> None:
        self.__chat_mediator_id: Final[str] = mediator_id
        self.__colleagues: Dict[str, 'Colleague'] = dict()

    def get_colleague(self, colleague_id: str) -> Optional['Colleague']:
        return self.__colleagues.get(colleague_id, None)

    def get_colleagues(self) -> Set['Colleague']:
        return set(self.__colleagues.values())

    def register_colleague(self, colleague: 'Colleague') -> None:
        if colleague not in self.__colleagues:
            self.__colleagues[colleague.get_colleague_id()] = colleague

    @abstractmethod
    def send_message(self, message: Dict[str, Any], sender_colleague_id: str, receiver_colleague_id: str) -> None:
        pass

    @abstractmethod
    def broadcast_message(self, message: Dict[str, Any], sender_colleague_id: str) -> None:
        pass
