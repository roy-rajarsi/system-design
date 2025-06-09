from threading import Lock
from typing import Final


class Account:

    def __init__(self, account_id: str, account_holder_name: str, balance: float) -> None:
        self.__account_id: Final[str] = account_id
        self.__account_holder_name: Final[str] = account_holder_name
        self.__balance: float = balance
        self.__lock: Lock = Lock()

    def get_account_id(self) -> str:
        return self.__account_id

    def get_account_holder_name(self) -> str:
        return self.__account_holder_name

    def get_balance(self) -> float:
        with self.__lock:
            return self.__balance

    def increment_balance(self, increment_by: float) -> None:
        with self.__lock:
            self.__balance += increment_by

    def decrement_balance(self, decrement_by: float) -> None:
        with self.__lock:
            self.__balance += decrement_by

    def __repr__(self) -> str:
        return f'Account(Id: {self.__account_id} AccountHolderName: {self.__account_holder_name} Balance: {self.__balance})'
