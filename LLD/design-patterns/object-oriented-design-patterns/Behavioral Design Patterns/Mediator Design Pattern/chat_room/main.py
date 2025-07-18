from colleague.chat_participant import ChatParticipant
from mediator.chat_room_mediator import ChatRoomMediator


def main() -> None:
    chat_room: ChatRoomMediator = ChatRoomMediator(mediator_id='1234', chat_room_name='Goats')

    ronaldo: ChatParticipant = ChatParticipant(colleague_id='ronaldo', mediator=chat_room, name='Ronaldo', department='RMA')
    messi: ChatParticipant = ChatParticipant(colleague_id='messi', mediator=chat_room, name='Messi', department='FCB')
    neymar: ChatParticipant = ChatParticipant(colleague_id='neymar', mediator=chat_room, name='Neymar', department='FCB')
    lewandowski: ChatParticipant = ChatParticipant(colleague_id='lewandowski', mediator=chat_room, name='Lewandowski', department='BAY')

    chat_room.register_colleague(colleague=ronaldo)
    chat_room.register_colleague(colleague=messi)
    chat_room.register_colleague(colleague=neymar)
    chat_room.register_colleague(colleague=lewandowski)

    print(chat_room)

    ronaldo.broadcast_message(message={'payload': 'Me and Messi are the GOATs !'})
    neymar.send_message(message={'payload': 'STFU'}, receiver_colleague_id=ronaldo.get_colleague_id())

    chat_room.block_sender(sender_colleague_id=neymar.get_colleague_id(), receiver_colleague_id=ronaldo.get_colleague_id())

    print(chat_room)

    neymar.broadcast_message(message={'payload': 'I am great !'})
    lewandowski.broadcast_message(message={'payload': 'Chill Bro !'})

    messi.send_message(message={'payload': 'Lets meet for dinner !'}, receiver_colleague_id=ronaldo.get_colleague_id())


if __name__ == '__main__':
    main()
