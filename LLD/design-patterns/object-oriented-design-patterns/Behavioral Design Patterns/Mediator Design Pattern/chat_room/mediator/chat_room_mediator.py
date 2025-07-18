from typing import Final, Set, Dict, override, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from colleague.colleague import Colleague

from mediator.mediator import Mediator


class ChatRoomMediator(Mediator):

    def __init__(self, mediator_id: str, chat_room_name: str) -> None:
        super().__init__(mediator_id=mediator_id)
        self.__chat_room_name: Final[str] = chat_room_name
        self.__blocked_lists: Dict[Colleague, Set['Colleague']] = dict()

    @override
    def register_colleague(self, colleague: 'Colleague') -> None:
        super().register_colleague(colleague=colleague)
        self.__blocked_lists[colleague] = set()

    @override
    def send_message(self, message: Dict[str, Any], sender_colleague_id: str, receiver_colleague_id: str) -> None:
        print(f'\nPRIVATE MESSAGE :: {sender_colleague_id} -> {receiver_colleague_id}\n')
        sender: Optional['Colleague'] = self.get_colleague(colleague_id=sender_colleague_id)
        receiver: Optional['Colleague'] = self.get_colleague(colleague_id=receiver_colleague_id)

        if sender is None or receiver is None or receiver in self.__blocked_lists.get(sender, list()):
            return

        receiver.receive_message_callback(message=message, sender_colleague_id=sender_colleague_id)

    @override
    def broadcast_message(self, message: Dict[str, Any], sender_colleague_id: str) -> None:
        print(f'\nBROADCAST MESSAGE from {sender_colleague_id}\n')
        sender: Optional['Colleague'] = self.get_colleague(colleague_id=sender_colleague_id)
        for receiver in self.get_colleagues():
            if sender not in self.__blocked_lists.get(receiver, list()):
                receiver.receive_message_callback(message=message, sender_colleague_id=sender_colleague_id)

    def block_sender(self, sender_colleague_id: str, receiver_colleague_id: str) -> None:
        sender: Optional['Colleague'] = self.get_colleague(colleague_id=sender_colleague_id)
        receiver: Optional['Colleague'] = self.get_colleague(colleague_id=receiver_colleague_id)

        if sender is None or receiver is None:
            return
        self.__blocked_lists.get(receiver).add(sender)
        print(f'\nBlocked {sender_colleague_id} -> {receiver_colleague_id}', self.__blocked_lists, '\n')

    @override
    def __repr__(self) -> str:
        return f'Chat Room :: Participants: {[colleague.get_colleague_id() for colleague in self.get_colleagues()]} Block Lists: {self.__blocked_lists}'
