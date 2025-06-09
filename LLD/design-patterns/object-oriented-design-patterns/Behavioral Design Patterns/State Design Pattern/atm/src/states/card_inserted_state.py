from typing import Optional, TYPE_CHECKING, override

if TYPE_CHECKING:
    from context.transaction_context import TransactionContext

from db.accounts import Accounts
from exceptions.illegal_transition_on_state_exception import IllegalTransitionOnStateException
from models.account import Account
from models.card import Card
from states.card_authenticated_state import CardAuthenticatedState
from states.card_not_authenticated_state import CardNotAuthenticatedState
from states.transaction_state import TransactionState
from transaction.transaction import Transaction


class CardInsertedState(TransactionState):

    @override
    def add_card_to_transaction_context(self, transaction_context: 'TransactionContext', card: Card) -> None:
        raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authenticate_card_in_transaction_context(self, transaction_context: 'TransactionContext', pin: int) -> None:
        if type(transaction_context.get_transaction_state()) is not CardInsertedState:
            raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

        account: Optional[Account] = Accounts().authenticate(card_number=transaction_context.get_card().get_number(), pin=pin)
        transaction_context.add_transaction_log(key='Card Authenticated', value=account is not None)
        if account is None:
            transaction_context.set_transaction_state(transaction_state=CardNotAuthenticatedState())
            return None

        transaction_context.set_account(account=account)
        transaction_context.set_transaction_state(transaction_state=CardAuthenticatedState())

    @override
    def add_transaction_to_transaction_context(self, transaction_context: 'TransactionContext', transaction: Transaction):
        raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def authorize_transaction(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def transact(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def reset_transaction_context(self, transaction_context: 'TransactionContext'):
        raise IllegalTransitionOnStateException(expected_state=CardInsertedState(), actual_state=transaction_context.get_transaction_state())

    @override
    def __repr__(self) -> str:
        return f'CardInsertedState'
