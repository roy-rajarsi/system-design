from enum import Enum


class TransactionType(Enum):
    BALANCE_CHECK_TRANSACTION = 1
    MONEY_DEPOSIT_TRANSACTION = 2
    MONEY_WITHDRAW_TRANSACTION = 3
    INVALID = -1

    @classmethod
    def get_transaction_type_from_value(cls, value: int) -> 'TransactionType':
        for transaction_type in cls:
            if transaction_type.value == value:
                return transaction_type
        return TransactionType.INVALID
