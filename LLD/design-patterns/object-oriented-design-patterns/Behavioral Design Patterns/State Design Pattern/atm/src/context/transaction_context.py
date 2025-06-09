from typing import Any, Dict, Optional

from models.account import Account
from models.card import Card
from states.idle_state import IdleState
from states.transaction_state import TransactionState
from transaction.transaction import Transaction


class TransactionContext:

    def __init__(self) -> None:
        self.__transaction_state: TransactionState = IdleState()
        self.__card: Optional[Card] = None
        self.__account: Optional[Account] = None
        self.__transaction: Optional[Transaction] = None
        self.__transaction_logs: Dict[str, Any] = dict()

    def get_transaction_state(self) -> TransactionState:
        return self.__transaction_state

    def set_transaction_state(self, transaction_state: TransactionState = IdleState()) -> None:
        self.__transaction_state = transaction_state

    def get_card(self) -> Optional[Card]:
        return self.__card

    def set_card(self, card: Card = None) -> None:
        self.__card = card

    def get_account(self) -> Optional[Account]:
        return self.__account

    def set_account(self, account: Account = None) -> None:
        self.__account = account

    def get_transaction(self) -> Optional[Transaction]:
        return self.__transaction

    def set_transaction(self, transaction: Transaction = None) -> None:
        self.__transaction = transaction

    def get_transaction_logs(self) -> Dict[str, Any]:
        return self.__transaction_logs

    def add_transaction_log(self, key: str, value: Any) -> None:
        self.__transaction_logs[key] = value

    def clear_transaction_logs(self):
        self.__transaction_logs.clear()

    def insert_card(self, card: Card) -> None:
        self.__transaction_state.add_card_to_transaction_context(transaction_context=self, card=card)

    def authenticate_card(self, pin: int) -> None:
        self.__transaction_state.authenticate_card_in_transaction_context(transaction_context=self, pin=pin)

    def init_transaction(self, transaction: Transaction) -> None:
        self.__transaction_state.add_transaction_to_transaction_context(transaction_context=self, transaction=transaction)

    def authorize_transaction(self) -> None:
        self.__transaction_state.authorize_transaction(transaction_context=self)

    def transact(self) -> None:
        self.__transaction_state.transact(transaction_context=self)

    def reset_transaction_context(self) -> None:
        self.__transaction_state.reset_transaction_context(transaction_context=self)
