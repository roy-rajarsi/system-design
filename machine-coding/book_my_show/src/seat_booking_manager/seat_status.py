from typing import Dict, Final, List, Optional

from booking.booking import Booking
from enums.seat_availability import SeatAvailability
from theatre.seat import Seat


class SeatStatus:

    def __init__(self, seat: Seat) -> None:
        self.__seat: Final[Seat] = seat
        self.__seat_availability: SeatAvailability = SeatAvailability.AVAILABLE
        self.__seat_booking: Optional[Booking] = None

    def get_seat_availability(self) -> SeatAvailability:
        return self.__seat_availability

    def set_seat_availability(self, seat_availability: SeatAvailability) -> None:
        self.__seat_availability = seat_availability

    def get_seat_booking(self) -> Optional[Booking]:
        return self.__seat_booking

    def set_seat_booking(self, seat_booking: Optional[Booking]) -> None:
        self.__seat_booking = seat_booking


class SeatStatusStore:

    def __init__(self, seats: List[Seat]) -> None:
        self.__seat_status_store: Dict[Seat, SeatStatus] = {seat: SeatStatus(seat=seat) for seat in seats}

    def get_seat_availability(self, seat: Seat) -> SeatAvailability:
        if self.__seat_status_store.get(seat, None) is not None:
            return self.__seat_status_store.get(seat).get_seat_availability()
        else:
            # raise SeatNotPresentInSeatStatusStoreException()
            raise Exception('SeatNotPresentInSeatStatusStoreException')

    def get_seat_booking(self, seat: Seat) -> Booking:
        if self.__seat_status_store.get(seat, None) is not None:
            return self.__seat_status_store.get(seat).get_seat_booking()
        else:
            # raise SeatNotPresentInSeatStatusStoreException()
            raise Exception('SeatNotPresentInSeatStatusStoreException')

    def set_seat_availability(self, seat: Seat, seat_availability: SeatAvailability) -> None:
        if self.__seat_status_store.get(seat, None) is not None:
            return self.__seat_status_store.get(seat).set_seat_availability(seat_availability=seat_availability)
        else:
            # raise SeatNotPresentInSeatStatusStoreException()
            raise Exception('SeatNotPresentInSeatStatusStoreException')

    def set_seat_booking(self, seat: Seat, seat_booking: Optional[Booking]) -> None:
        if self.__seat_status_store.get(seat, None) is not None:
            return self.__seat_status_store.get(seat).set_seat_booking(seat_booking=seat_booking)
        else:
            # raise SeatNotPresentInSeatStatusStoreException()
            raise Exception('SeatNotPresentInSeatStatusStoreException')
