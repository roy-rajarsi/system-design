from decimal import Decimal
from enum import Enum


class Currency(Enum):
    CURRENCY_INR = 'CURRENCY_INR'
    CURRENCY_USD = 'CURRENCY_USD'


class Money:

    def __init__(self, amount: Decimal, currency: Currency) -> None:
        self.__amount: Decimal = amount
        self.__currency: Currency = currency

    def get_amount(self) -> Decimal:
        return self.__amount

    def get_currency(self) -> Currency:
        return self.__currency

    def __repr__(self) -> str:
        return f'Money: {self.__amount}{self.__currency})'
