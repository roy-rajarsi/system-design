from abc import ABC, abstractmethod
from typing import Any, Dict, Final

from models.account import Account


class Transaction(ABC):

    def __init__(self, account: Account) -> None:
        self.__account: Final[Account] = account
        self.__transaction_result: Final[Dict[str, Any]] = dict()

    def get_account(self) -> Account:
        return self.__account

    def get_transaction_result(self) -> Dict[str, Any]:
        return self.__transaction_result

    def add_transaction_result(self, key: str, value: Any) -> None:
        self.__transaction_result[key] = value

    @abstractmethod
    def authorize(self) -> bool:
        pass

    @abstractmethod
    def transact(self) -> None:
        pass
