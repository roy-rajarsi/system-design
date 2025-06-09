from typing import TYPE_CHECKING, override

from states.transaction_not_authorized_state import TransactionNotAuthorizedState

if TYPE_CHECKING:
    from context.transaction_context import TransactionContext

from exceptions.illegal_transition_on_state_exception import IllegalTransitionOnStateException
from models.card import Card
from states.transaction_authorized_state import TransactionAuthorizedState
from states.transaction_state import TransactionState
from transaction.transaction import Transaction


class TransactionInitialisedState(TransactionState):

    @override
    def add_card_to_transaction_context(self, transaction_context: 'TransactionContext', card: Card) -> None:
        raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authenticate_card_in_transaction_context(self, transaction_context: 'TransactionContext', pin):
        raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def add_transaction_to_transaction_context(self, transaction_context: 'TransactionContext', transaction: Transaction):
        raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authorize_transaction(self, transaction_context: 'TransactionContext'):
        if type(transaction_context.get_transaction_state()) is not TransactionInitialisedState:
            raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

        transaction_authorized: bool = transaction_context.get_transaction().authorize()
        transaction_context.add_transaction_log(key='Transaction Authorized', value=transaction_authorized)
        transaction_context.set_transaction_state(transaction_state=TransactionAuthorizedState() if transaction_authorized else TransactionNotAuthorizedState())

    @override
    def transact(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def reset_transaction_context(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=TransactionInitialisedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def __repr__(self) -> str:
        return f'TransactionInitialisedState'
