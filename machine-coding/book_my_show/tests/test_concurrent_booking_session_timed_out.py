from datetime import timedelta as TimeDelta
from datetime import datetime as DateTime
from pytest import mark
from time import sleep
from typing import List
from uuid import UUID

from src.show.show import Show
from src.show.show_metadata import ShowMetaData
from src.theatre.theatre import Theatre
from src.theatre.auditorium import Auditorium
from src.theatre.seat import Seat
from src.users.user import User


class TestConcurrentBookingSessionTimedOut:

    def setup_method(self) -> None:
        self.theatre: Theatre = Theatre()
        self.theatre.add_auditorium(auditorium_number=1)
        self.theatre.add_auditorium(auditorium_number=2)
        self.auditorium_1: Auditorium = self.theatre.get_auditoriums()[0]
        self.auditorium_2: Auditorium = self.theatre.get_auditoriums()[1]

        for row in range(5):
            for col in range(5):
                self.auditorium_1.add_seat(row=row, column=col)
                self.auditorium_2.add_seat(row=row, column=col)

        self.show1: Show = Show(show_metadata=ShowMetaData(show_name='Gupi Bagha',
                                                           show_start_time=DateTime.now(),
                                                           show_end_time=DateTime.now() + TimeDelta(hours=2, minutes=30)),
                                auditorium=self.auditorium_1)
        self.show2: Show = Show(show_metadata=ShowMetaData(show_name='Golpo Holeo Sotti',
                                                           show_start_time=DateTime.now(),
                                                           show_end_time=DateTime.now() + TimeDelta(hours=3)),
                                auditorium=self.auditorium_2)

        self.user1: User = User(username='User1')
        self.user2: User = User(username='User2')

    @mark.slow
    def test_concurrent_booking_session_timed_out(self) -> None:

        # User1 Request
        show1_available_seats_user1: List[Seat] = self.show1.get_available_seats()
        session_id: UUID = self.show1.book_seats(user=self.user1, seats=show1_available_seats_user1[0:5])

        # User2 Request
        show1_available_seats_user2: List[Seat] = self.show1.get_available_seats()
        assert show1_available_seats_user1[5:] == show1_available_seats_user2

        # Payment of User1 Fails and Session Timed Out
        sleep(10)
        assert not self.show1.confirm_seats(session_id=session_id)

        # User2 sees all the seats
        show1_available_seats_user2_request2: List[Seat] = self.show1.get_available_seats()
        assert show1_available_seats_user1 == show1_available_seats_user2_request2

    def teardown_method(self) -> None:
        del self.theatre
        del self.auditorium_1
        del self.auditorium_2
        del self.show1
        del self.show2
        del self.user1
        del self.user2
