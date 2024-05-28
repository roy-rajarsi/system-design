from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, override


class ExpenseResponse(ABC):

    def __init__(self, response: Dict[str, Any]) -> None:
        self.__response: Dict[str, Any] = response

    def get_response_as_dict(self) -> Dict[str, Any]:
        return deepcopy(self.__response)

    @staticmethod
    @abstractmethod
    def validate_expense_response(response: Dict[str, Any]):
        pass

    def __repr__(self) -> str:
        return f'ExpenseResponse({self.get_response_as_dict()})'


class ExpensePercentageValidationResponse(ExpenseResponse):

    def __init__(self, response: Dict[str, Any]) -> None:
        self.validate_expense_response(response=response)
        super().__init__(response=response)

    @staticmethod
    @override
    def validate_expense_response(response: Dict[str, Any]):
        if 'is_valid_expense_percentage_distribution' not in response:
            raise Exception(f'\'is_valid_expense_percentage_distribution\' must be present in ExpensePercentageValidationResponse')


class PayorDebtorExpenseRelationshipGenerationResponse(ExpenseResponse):

    def __init__(self, response: Dict[str, Any]) -> None:
        self.validate_expense_response(response=response)
        super().__init__(response=response)

    @staticmethod
    @override
    def validate_expense_response(response: Dict[str, Any]):
        if 'payor_debtor_expense_relationship' not in response:
            raise Exception(f'No payor_debtor_expense_relationship in Expense Response')


class SaveExpenseResponse(ExpenseResponse):

    def __init__(self, response: Dict[str, Any]) -> None:
        self.validate_expense_response(response=response)
        super().__init__(response=response)

    @staticmethod
    @override
    def validate_expense_response(response: Dict[str, Any]):
        pass
