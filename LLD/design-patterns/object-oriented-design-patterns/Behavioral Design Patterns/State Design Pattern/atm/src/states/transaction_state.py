from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, override
if TYPE_CHECKING:
    from context.transaction_context import TransactionContext

from models.card import Card
from transaction.transaction import Transaction


class TransactionState(ABC):

    @abstractmethod
    def add_card_to_transaction_context(self, transaction_context: 'TransactionContext', card: Card) -> None:
        pass

    @abstractmethod
    def authenticate_card_in_transaction_context(self, transaction_context: 'TransactionContext', pin):
        pass

    @abstractmethod
    def add_transaction_to_transaction_context(self, transaction_context: 'TransactionContext', transaction: Transaction):
        pass

    @abstractmethod
    def authorize_transaction(self, transaction_context: 'TransactionContext'):
        pass

    @abstractmethod
    def transact(self, transaction_context: 'TransactionContext'):
        pass

    @abstractmethod
    def reset_transaction_context(self, transaction_context: 'TransactionContext'):
        pass

    @override
    def __repr__(self) -> str:
        return f'TransactionState'
