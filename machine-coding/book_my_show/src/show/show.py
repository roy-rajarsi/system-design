from typing import Final, List, Optional
from uuid import UUID

from .show_metadata import ShowMetaData
from seat_booking_manager.seat_booking_manager import SeatBookingManager
from theatre.auditorium import Auditorium
from theatre.seat import Seat
from users.user import User


class Show:

    def __init__(self, show_metadata: ShowMetaData, auditorium: Auditorium) -> None:
        self.__show_metadata: ShowMetaData = show_metadata
        self.__auditorium: Final[Auditorium] = auditorium
        self.__seat_booking_manager: Final[SeatBookingManager] = SeatBookingManager(show_metadata=show_metadata, seats=self.__auditorium.get_seats())

    def get_auditorium(self) -> Auditorium:
        return self.__auditorium

    def get_available_seats(self) -> List[Seat]:
        return self.__seat_booking_manager.get_available_seats()

    def book_seats(self, user: User, seats: List[Seat]) -> Optional[UUID]:
        session_id: Optional[UUID] = self.__seat_booking_manager.book_seats(user=user, seats=seats)
        if session_id is None:
            print(f'One or More Selected Seats is/are NOT Available Currently. Please select different seats')
        else:
            print(f'{seats} are reserved for {user} for sometime...Please proceed to Payment')
        return session_id

    def cancel_seat_reservation(self, session_id: UUID) -> None:
        self.__seat_booking_manager.cancel_seat_booking(session_id=session_id)

    def confirm_seats(self, session_id: UUID) -> bool:
        return self.__seat_booking_manager.confirm_seat_booking(session_id=session_id)
