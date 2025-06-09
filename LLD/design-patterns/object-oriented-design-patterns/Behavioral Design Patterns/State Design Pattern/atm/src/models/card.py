from typing import Final


class Card:

    def __init__(self, card_number: str, name: str, expiry_month: int, expiry_year: int) -> None:
        self.__number: Final[str] = card_number
        self.__name: Final[str] = name
        self.__expiry_month: Final[int] = expiry_month
        self.__expiry_year: Final[int] = expiry_year

    def get_number(self) -> str:
        return self.__number

    def get_name(self) -> str:
        return self.__name

    def get_expiry_month(self) -> int:
        return self.__expiry_month

    def get_expiry_year(self) -> int:
        return self.__expiry_year

    def __repr__(self) -> str:
        return f'Card(Number: {self.__number}, Name: {self.__name}, Expiry: ({self.__expiry_month}, {self.__expiry_year}))'
