from group_expense_distribution_strategy import GroupExpenseDistributionStrategy
from group_expense_distribution_strategies import GroupExpenseDistributionStrategies
from expense.services.money import Money

from decimal import Decimal
from typing import Dict, List, Optional, override


class GroupExpenseDistributionStrategyPercentageDistribution(GroupExpenseDistributionStrategy):

    def __init__(self) -> None:
        super().__init__(group_expense_distribution_strategy=GroupExpenseDistributionStrategies.GROUP_EXPENSE_DISTRIBUTION_STRATEGY_PERCENTAGE)

    @override
    def generate_debtor_user_id_to_money_owed_map(self, debtor_list: List[int], expense: Money, expense_distribution_percentage_list: Optional[List[Decimal]] = None) -> Dict[int, Money]:
        return {debtor_user_id: Money(amount=expense.get_amount()*expense_percent/100,
                                      currency=expense.get_currency())
                for debtor_user_id, expense_percent in zip(debtor_list, expense_distribution_percentage_list)}
