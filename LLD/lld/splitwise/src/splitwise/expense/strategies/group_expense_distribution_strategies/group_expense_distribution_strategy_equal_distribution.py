from group_expense_distribution_strategy import GroupExpenseDistributionStrategy
from group_expense_distribution_strategies import GroupExpenseDistributionStrategies
from expense.services.money import Money

from decimal import Decimal
from typing import Dict, List, Optional, override


class GroupExpenseDistributionStrategyEqualDistribution(GroupExpenseDistributionStrategy):

    def __init__(self) -> None:
        super().__init__(group_expense_distribution_strategy=GroupExpenseDistributionStrategies.GROUP_EXPENSE_DISTRIBUTION_STRATEGY_EQUAL)

    @override
    def generate_debtor_user_id_to_money_owed_map(self, debtor_list: List[int], expense: Money, expense_distribution_percentage_list: Optional[List[Decimal]] = None) -> Dict[int, Money]:
        money_owed_per_debtor: Money = Money(amount=expense.get_amount() / len(debtor_list), currency=expense.get_currency())

        return {debtor_user_id: money_owed_per_debtor for debtor_user_id in debtor_list}
