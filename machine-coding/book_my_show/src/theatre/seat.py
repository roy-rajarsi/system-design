from typing import Final


class Seat:

    def __init__(self, auditorium_number: int, row: int, column: int) -> None:
        self.__auditorium_number: int = auditorium_number
        self.__row: Final[int] = row
        self.__column: Final[int] = column

    def get_auditorium_number(self) -> int:
        return self.__auditorium_number

    def get_row(self) -> int:
        return self.__row

    def get_col(self) -> int:
        return self.__column

    def __repr__(self) -> str:
        return f'Seat({self.__row}, {self.__column})'
