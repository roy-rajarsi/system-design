from typing import Final, override

from models.account import Account
from transaction.transaction import Transaction


class MoneyWithdrawTransaction(Transaction):

    def __init__(self, account: Account, money_to_withdraw: float) -> None:
        super().__init__(account=account)
        self.__money_to_withdraw: Final[float] = money_to_withdraw

    def authorize(self) -> bool:
        return self.__money_to_withdraw <= self.get_account().get_balance()

    @override
    def transact(self) -> None:
        self.get_account().decrement_balance(decrement_by=self.__money_to_withdraw)
        self.add_transaction_result(key='Balance', value=self.get_account().get_balance())
        self.add_transaction_result(key='Money Withdrawn', value=self.__money_to_withdraw)
