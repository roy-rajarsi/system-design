from typing import TYPE_CHECKING, override

from models.card import Card

if TYPE_CHECKING:
    from context.transaction_context import TransactionContext

from exceptions.illegal_transition_on_state_exception import IllegalTransitionOnStateException
from states.transaction_initialised_state import TransactionInitialisedState
from states.transaction_state import TransactionState
from transaction.transaction import Transaction


class CardAuthenticatedState(TransactionState):

    @override
    def add_card_to_transaction_context(self, transaction_context: 'TransactionContext', card: Card) -> None:
        raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authenticate_card_in_transaction_context(self, transaction_context: 'TransactionContext', pin):
        raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def add_transaction_to_transaction_context(self, transaction_context: 'TransactionContext', transaction: Transaction):
        if type(transaction_context.get_transaction_state()) is not CardAuthenticatedState:
            raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

        transaction_context.set_transaction(transaction=transaction)
        transaction_context.set_transaction_state(transaction_state=TransactionInitialisedState())

    @override
    def authorize_transaction(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def transact(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def reset_transaction_context(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardAuthenticatedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def __repr__(self) -> str:
        return f'CardAuthenticatedState'

