from typing import Final, List

from .seat import Seat


class Auditorium:

    def __init__(self, auditorium_number: int) -> None:
        self.__auditorium_number: Final[int] = auditorium_number
        self.__seats: List[Seat] = list()

    def add_seat(self, row: int, column: int) -> None:
        self.__seats.append(Seat(auditorium_number=self.__auditorium_number, row=row, column=column))

    def get_seats(self) -> List[Seat]:
        return [seat for seat in self.__seats]
