from datetime import timedelta as TimeDelta
from datetime import datetime as DateTime
from typing import List
from uuid import UUID

from payment.payment_store import PaymentStore
from show.show import Show
from show.show_metadata import ShowMetaData
from theatre.theatre import Theatre
from theatre.auditorium import Auditorium
from theatre.seat import Seat
from users.user import User


# Happy Use Case for Testing


theatre: Theatre = Theatre()
theatre.add_auditorium(auditorium_number=1)
theatre.add_auditorium(auditorium_number=2)
auditorium_1: Auditorium = theatre.get_auditoriums()[0]
auditorium_2: Auditorium = theatre.get_auditoriums()[1]

for row in range(5):
    for col in range(5):
        auditorium_1.add_seat(row=row, column=col)
        auditorium_2.add_seat(row=row, column=col)

show1: Show = Show(show_metadata=ShowMetaData(show_name='Gupi Bagha',
                                                   show_start_time=DateTime.now(),
                                                   show_end_time=DateTime.now() + TimeDelta(hours=2, minutes=30)),
                        auditorium=auditorium_1)
show2: Show = Show(show_metadata=ShowMetaData(show_name='Golpo Holeo Sotti',
                                                   show_start_time=DateTime.now(),
                                                   show_end_time=DateTime.now() + TimeDelta(hours=3)),
                        auditorium=auditorium_2)

user1: User = User(username='User1')
user2: User = User(username='User2')


# User1 Request
show1_available_seats_user1: List[Seat] = show1.get_available_seats()
session_id_user1: UUID = show1.book_seats(user=user1, seats=show1_available_seats_user1[0:5])
print('U1 Sess:', session_id_user1)

# User2 Request
show1_available_seats_user2: List[Seat] = show1.get_available_seats()
assert show1_available_seats_user1[5:] == show1_available_seats_user2
session_id_user2: UUID = show1.book_seats(user=user2, seats=show1_available_seats_user2[0:5])
print('U2 Sess:', session_id_user2)

print(PaymentStore.get_all_sessions())

# User2 Payment Succeeds
PaymentStore.pay(session_id=session_id_user2)
print(PaymentStore.get_all_sessions())
assert show1.confirm_seats(session_id=session_id_user2)

# User1 Payment Succeeds
PaymentStore.pay(session_id=session_id_user1)
print(PaymentStore.get_all_sessions())
assert show1.confirm_seats(session_id=session_id_user1)

    