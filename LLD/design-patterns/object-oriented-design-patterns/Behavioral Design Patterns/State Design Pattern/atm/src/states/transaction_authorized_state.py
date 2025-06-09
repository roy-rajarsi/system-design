from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from context.transaction_context import TransactionContext

from exceptions.illegal_transition_on_state_exception import IllegalTransitionOnStateException
from models.card import Card
from states.transaction_completed_state import TransactionCompletedState
from states.transaction_state import TransactionState
from transaction.transaction import Transaction


class TransactionAuthorizedState(TransactionState):

    @override
    def add_card_to_transaction_context(self, transaction_context: 'TransactionContext', card: Card) -> None:
        raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authenticate_card_in_transaction_context(self, transaction_context: 'TransactionContext', pin):
        raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def add_transaction_to_transaction_context(self, transaction_context: 'TransactionContext', transaction: Transaction):
        raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authorize_transaction(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def transact(self, transaction_context: 'TransactionContext'):
        if type(transaction_context.get_transaction_state()) is not TransactionAuthorizedState:
            raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

        transaction_context.get_transaction().transact()
        for key, value in transaction_context.get_transaction().get_transaction_result().items():
            transaction_context.add_transaction_log(key=key, value=value)
        transaction_context.set_transaction_state(transaction_state=TransactionCompletedState())

    @override
    def reset_transaction_context(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=TransactionAuthorizedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def __repr__(self) -> str:
        return f'TransactionAuthorizedState'
