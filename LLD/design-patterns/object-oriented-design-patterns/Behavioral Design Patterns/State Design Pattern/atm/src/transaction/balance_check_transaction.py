from typing import override

from models.account import Account
from transaction.transaction import Transaction


class BalanceCheckTransaction(Transaction):

    def __init__(self, account: Account) -> None:
        super().__init__(account=account)

    @override
    def authorize(self) -> bool:
        return True

    @override
    def transact(self) -> None:
        self.add_transaction_result(key='Balance', value=self.get_account().get_balance())
