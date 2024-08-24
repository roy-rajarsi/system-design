from threading import Lock
from typing import Final, List, Optional
from uuid import UUID

from booking.booking import Booking
from enums.seat_availability import SeatAvailability
from payment.payment_store import PaymentStore
from .seat_status import SeatStatusStore
from session.session import Session
from session.session_store import SessionStore
from show.show_metadata import ShowMetaData
from theatre.seat import Seat
from users.user import User


class SeatBookingManager:

    def __init__(self, show_metadata: ShowMetaData, seats: List[Seat]) -> None:
        self.__show_metadata: Final[ShowMetaData] = show_metadata
        self.__seats: List[Seat] = seats
        self.__seat_booking_session_store: SessionStore = SessionStore()
        self.__seat_status_store: SeatStatusStore = SeatStatusStore(seats=self.__seats)
        self.__seat_booking_lock: Lock = Lock()

    def get_show_metadata(self) -> ShowMetaData:
        return self.__show_metadata

    def get_available_seats(self) -> List[Seat]:
        available_seats: List[Seat] = list()
        self.__seat_booking_lock.acquire(blocking=True, timeout=-1)
        seat: Seat
        for seat in self.__seats:
            if self.__seat_status_store.get_seat_availability(seat=seat) == SeatAvailability.AVAILABLE:
                available_seats.append(seat)
        self.__seat_booking_lock.release()
        return available_seats

    def book_seats(self, user: User, seats: List[Seat]) -> Optional[UUID]:
        seat_booking_session: Optional[Session] = None
        self.__seat_booking_lock.acquire(blocking=True, timeout=-1)
        if self.__are_seats_available(seats=seats):
            seat_booking_session: Session = Session(user=user, session_payload={'seats': seats, 'payment': 'incomplete'})
            self.__seat_booking_session_store.add_session(session=seat_booking_session)
            PaymentStore.add_session(session=seat_booking_session)
            self.__lock_seats_for_user(user=user, seats=seats)
        self.__seat_booking_lock.release()
        return seat_booking_session.get_session_id() if seat_booking_session is not None else None

    def __are_seats_available(self, seats: List[Seat]) -> bool:
        seat: Seat
        for seat in seats:
            if self.__seat_status_store.get_seat_availability(seat=seat) != SeatAvailability.AVAILABLE:
                return False
        return True

    def __lock_seats_for_user(self, user: User, seats: List[Seat]) -> None:
        seat: Seat
        for seat in seats:
            self.__seat_status_store.set_seat_availability(seat=seat, seat_availability=SeatAvailability.TEMPORARILY_UNAVAILABLE)
            self.__seat_status_store.set_seat_booking(seat=seat, seat_booking=Booking(
                seat=seat,
                show_metadata=self.__show_metadata,
                user=user
            ))

    def cancel_seat_booking(self, session_id: UUID) -> None:
        session: Session = self.__seat_booking_session_store.get_session(session_id=session_id)
        session.expire_session()
        seats: List[Seat] = session.get_session_payload().get('seats')
        seat: Seat
        for seat in seats:
            self.__seat_status_store.set_seat_availability(seat=seat, seat_availability=SeatAvailability.AVAILABLE)
            self.__seat_status_store.set_seat_booking(seat=seat, seat_booking=None)

    def confirm_seat_booking(self, session_id: UUID) -> bool:
        session: Session = self.__seat_booking_session_store.get_session(session_id=session_id)
        print(f'Confirm:: Session -> {session}')
        if session is None:
            print(f'Invalid SessionId - {session_id}')
            return False
        elif session.is_expired():
            print(f'Session - {session_id} Expired. If money is debited from your account, please request for a refund !')
            self.cancel_seat_booking(session_id=session_id)
            return False
        elif session.get_session_payload().get('payment') == 'complete':
            self.__seat_booking_lock.acquire(blocking=True, timeout=-1)
            self.__confirm_seats(seats=session.get_session_payload().get('seats'))
            self.__seat_booking_lock.release()
            return True
        else:
            print('Please confirm payment, before sending confirm booking request')
            return False

    def __confirm_seats(self, seats: List[Seat]) -> None:
        seat: Seat
        for seat in seats:
            self.__seat_status_store.set_seat_availability(seat=seat, seat_availability=SeatAvailability.UNAVAILABLE)
            self.__seat_status_store.get_seat_booking(seat=seat).confirm_booking()
