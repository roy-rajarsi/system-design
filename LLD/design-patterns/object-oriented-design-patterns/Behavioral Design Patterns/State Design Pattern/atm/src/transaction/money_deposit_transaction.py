from typing import Final, override

from models.account import Account
from transaction.transaction import Transaction


class MoneyDepositTransaction(Transaction):

    def __init__(self, account: Account, money_to_deposit: float) -> None:
        super().__init__(account=account)
        self.__money_to_deposit: Final[float] = money_to_deposit

    @override
    def authorize(self) -> bool:
        return True

    @override
    def transact(self) -> None:
        self.get_account().increment_balance(increment_by=self.__money_to_deposit)
        self.add_transaction_result(key='Balance', value=self.get_account().get_balance())
        self.add_transaction_result(key='Money Deposited', value=self.__money_to_deposit)
