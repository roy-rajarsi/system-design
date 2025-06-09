from typing import Set, Type

from enums.transaction_type import TransactionType
from transaction.balance_check_transaction import BalanceCheckTransaction
from transaction.money_deposit_transaction import MoneyDepositTransaction
from transaction.money_withdraw_transaction import MoneyWithdrawTransaction
from transaction.transaction import Transaction


class TransactionFactory:
    __transaction_types: Set[TransactionType] = [transaction_type for transaction_type in TransactionType]

    @classmethod
    def get_transaction(cls, transaction_type: TransactionType) -> Type[Transaction]:
        if transaction_type == TransactionType.BALANCE_CHECK_TRANSACTION:
            return BalanceCheckTransaction
        elif transaction_type == TransactionType.MONEY_DEPOSIT_TRANSACTION:
            return MoneyDepositTransaction
        elif transaction_type == TransactionType.MONEY_WITHDRAW_TRANSACTION:
            return MoneyWithdrawTransaction

        raise InvalidTransactionTypeException(valid_types=cls.__transaction_types, requested_type=transaction_type)
