from states.transaction_state import TransactionState


class IllegalTransitionOnStateException(Exception):

    def __init__(self, expected_state: TransactionState, actual_state: TransactionState) -> None:
        super().__init__(f'Expected Context State :: {expected_state} Actual Context State :: {actual_state}')
