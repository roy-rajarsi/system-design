from uuid import uuid4, UUID

from enums.booking_status import BookingStatus
from show.show_metadata import ShowMetaData
from theatre.seat import Seat
from users.user import User


class Booking:

    def __init__(self, seat: Seat, show_metadata: ShowMetaData, user: User) -> None:
        self.__booking_id: UUID = uuid4()
        self.__seat: Seat = seat
        self.__show_metadata: ShowMetaData = show_metadata
        self.__user: User = user
        self.__booking_status: BookingStatus = BookingStatus.NOT_CONFIRMED

    def get_booking_id(self) -> UUID:
        return self.__booking_id

    def get_seat(self) -> Seat:
        return self.__seat

    def get_show_metadat(self) -> ShowMetaData:
        return self.__show_metadata

    def get_user(self) -> User:
        return self.__user

    def confirm_booking(self) -> None:
        self.__booking_status = BookingStatus.CONFIRMED
