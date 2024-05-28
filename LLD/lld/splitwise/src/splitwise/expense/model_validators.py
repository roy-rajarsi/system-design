from expense.services.money import Currency

from django.core.exceptions import ValidationError
from enum import Enum


class ExpenseValidator:

    class ExpenseType(Enum):
        EXPENSE_TYPE_GROUP_EXPENSE = 'EXPENSE_TYPE_GROUP_EXPENSE'
        EXPENSE_TYPE_NON_GROUP_EXPENSE = 'EXPENSE_TYPE_NON_GROUP_EXPENSE'

    @staticmethod
    def is_expense_currency_valid(expense_currency: str) -> None:
        if expense_currency not in [currency.value for currency in Currency]:
            raise ValidationError(f'Currency must from this list -> {[currency.value for currency in Currency]}')

    @staticmethod
    def is_expense_type_valid(expense_type: str) -> None:
        if expense_type not in [expense_type_.value for expense_type_ in ExpenseValidator.ExpenseType]:
            raise ValidationError(f'Expense Type must be from this list -> {[expense_type_.value for expense_type_ in ExpenseValidator.ExpenseType]}')


class GroupExpenseValidator:
    @staticmethod
    def is_money_distribution_strategy_valid(strategy: str) -> None:
        if strategy not in [group_expense_distribution_strategy.value
                            for group_expense_distribution_strategy in GroupExpenseValidator.GroupExpenseDistributionStrategy]:
            raise ValidationError(f'Group Expense Distribution Strategy must be from this list -> '
                                  f'{[group_expense_distribution_strategy.value for group_expense_distribution_strategy in GroupExpenseValidator.GroupExpenseDistributionStrategy]}')
