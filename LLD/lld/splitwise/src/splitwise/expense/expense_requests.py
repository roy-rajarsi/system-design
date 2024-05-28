from expense.model_validators import ExpenseValidator
from expense.strategies.group_expense_distribution_strategies.group_expense_distribution_strategies import GroupExpenseDistributionStrategies

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, override


class ExpenseRequest(ABC):

    def __init__(self, request: Dict[str, Any]):
        self.__request: Dict[str, Any] = request

    def get_request_as_dict(self) -> Dict[str, Any]:
        return deepcopy(self.__request)

    @staticmethod
    @abstractmethod
    def validate_expense_request(request: Dict[str, Any]):
        pass

    def __repr__(self) -> str:
        return f'ExpenseRequest({self.get_request_as_dict()})'


class ExpensePercentageValidationRequest(ExpenseRequest):

    def __init__(self, request: Dict[str, Any]) -> None:
        self.validate_expense_request(request=request)
        super().__init__(request=request)

    @staticmethod
    @override
    def validate_expense_request(request: Dict[str, Any]) -> None:
        if 'expense_percentage_map' in request.keys():

            user_id: int
            for user_id in request.get('expense_percentage_map'):
                expense_percentage: float = request.get('expense_percentage_map').get(user_id)
                if not (isinstance(expense_percentage, int) or isinstance(expense_percentage, float)):
                    raise Exception('Expense Percentage MUST be integer or float')

        else:
            raise Exception('No expense_percentage_map in ExpenseRequest')


class PayorDebtorExpenseRelationshipGenerationRequest(ExpenseRequest):

    def __init__(self, request: Dict[str, Any]) -> None:
        self.validate_expense_request(request=request)
        super().__init__(request=request)

    @staticmethod
    @override
    def validate_expense_request(request: Dict[str, Any]) -> None:
        if 'payor_user_id' not in request:
            raise Exception(f'No payor_user_id in ExpenseRequest')
        if 'debtor_list' not in request:
            raise Exception(f'No debtor_list in ExpenseRequest')
        if 'expense' not in request:
            raise Exception('No expense in ExpenseRequest')
        if 'expense_type' not in request:
            raise Exception('No expense_type in ExpenseRequest')
        if request.get('expense_type') == ExpenseValidator.ExpenseType.EXPENSE_TYPE_GROUP_EXPENSE.value:
            if 'expense_distribution_strategy' not in request:
                raise Exception('No expense_distribution_strategy in Expense Request')
            if request.get('expense_distribution_strategy') == GroupExpenseDistributionStrategies.GROUP_EXPENSE_DISTRIBUTION_STRATEGY_PERCENTAGE:
                if 'expense_distribution_percentage_list' not in request:
                    raise Exception('No expense_distribution_percentage_list in Expense Request')
        elif request.get('expense_type') == ExpenseValidator.ExpenseType.EXPENSE_TYPE_NON_GROUP_EXPENSE.value:
            if len(request.get('debtor_list')) > 1:
                raise Exception(f'More than one debtor in 1 NonGroup Expense Request')


class SaveExpenseRequest(ExpenseRequest):

    def __init__(self, request: Dict[str, Any]) -> None:
        self.validate_expense_request(request=request)
        super().__init__(request=request)

    @staticmethod
    @override
    def validate_expense_request(request: Dict[str, Any]) -> None:
        if 'payor_debtor_expense_relationship' not in request:
            raise Exception(f'No payor_debtor_expense_relationship in Expense Request')
