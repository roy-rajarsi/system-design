from amount_owed_in_group_map.amount_owed_in_group_map import AmountOwedInGroupMap
from expense.services.money import Money

from abc import ABC, abstractmethod


class MapGenerationStrategy(ABC):

    @staticmethod
    @abstractmethod
    def generate_minimum_transaction_count_map(amount_owed_map: AmountOwedInGroupMap) -> AmountOwedInGroupMap:
        pass

    @staticmethod
    def _is_money_owed(money: Money) -> bool:
        return money.get_amount() > 0
