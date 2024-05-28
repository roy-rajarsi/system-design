from expense.services.money import Money

from collections import namedtuple
from typing import Dict, Type


MoneyReceiver: Type['MoneyReceiver'] = namedtuple(typename='MoneyReceiver', field_names=['payor_user_id', 'money'])


class DebtSettlementMap:

    def __init__(self, debt_settlement_map: Dict[int, MoneyReceiver]) -> None:
        self.__debt_settlement_map: Dict[int, MoneyReceiver] = debt_settlement_map

    def get_debt_settlement_map(self) -> Dict[int, MoneyReceiver]:
        return self.__debt_settlement_map.copy()

    def add_possible_settlement(self, debtor_user_id: int, payor_user_id: int, money_to_be_transferred: Money) -> None:
        self.get_debt_settlement_map()[debtor_user_id] = MoneyReceiver(payor_user_id=payor_user_id, money=Money(amount=abs(money_to_be_transferred.get_amount()),
                                                                                                                currency=money_to_be_transferred.get_currency()))

    def drop_possible_settlement(self, debtor_user_id: int) -> None:
        self.get_debt_settlement_map().pop(debtor_user_id)

    def __repr__(self) -> str:
        return f'DebtSettlementMap({str(self.__debt_settlement_map)})'
