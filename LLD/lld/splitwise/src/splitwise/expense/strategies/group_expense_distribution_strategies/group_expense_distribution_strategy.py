from group_expense_distribution_strategies import GroupExpenseDistributionStrategies
from expense.services.money import Money

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List, Optional


class GroupExpenseDistributionStrategy(ABC):

    def __init__(self, group_expense_distribution_strategy: GroupExpenseDistributionStrategies) -> None:
        self.__group_expense_distribution_strategy: GroupExpenseDistributionStrategies = group_expense_distribution_strategy

    @staticmethod
    @abstractmethod
    def generate_debtor_user_id_to_money_owed_map(self, debtor_list: List[int], expense: Money, expense_distribution_percentage_list: Optional[List[Decimal]] = None) -> Dict[int, Money]:
        pass
