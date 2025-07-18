from typing import Final, override, Dict, Any

from chat_room.colleague.colleague import Colleague
from mediator.mediator import Mediator


class ChatParticipant(Colleague):

    def __init__(self, colleague_id: str, mediator: Mediator, name: str, department: str) -> None:
        super().__init__(colleague_id=colleague_id, mediator=mediator)
        self.__name: Final[str] = name
        self.__department: Final[str] = department

    def get_name(self) -> str:
        return self.__name

    def get__department(self) -> str:
        return self.__department

    @override
    def send_message(self, message: Dict[str, Any], receiver_colleague_id: str) -> None:
        self.get_mediator().send_message(message=message, sender_colleague_id=self.get_colleague_id(), receiver_colleague_id=receiver_colleague_id)

    @override
    def receive_message_callback(self, message: Dict[str, Any], sender_colleague_id: str) -> None:
        print(f'Message Received By {self.get_colleague_id()} :: Message: {message} From: {sender_colleague_id}')

    def broadcast_message(self, message: Dict[str, Any]) -> None:
        self.get_mediator().broadcast_message(message=message, sender_colleague_id=self.get_colleague_id())
