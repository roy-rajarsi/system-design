from expense.expense_requests import ExpenseRequest
from expense.expense_responses import ExpenseResponse

from abc import ABC, abstractmethod
from typing import Optional


class ExpenseHandler(ABC):

    def __init__(self) -> None:
        self.__next_handler: Optional[ExpenseHandler] = None

    def get_next_handler(self) -> 'ExpenseHandler':
        return self.__next_handler

    def set_next_handler(self, next_handler: 'ExpenseHandler') -> None:
        if self.__next_handler is not None:
            raise Exception(f'Expense Handler already has a next handler')

        self.__next_handler = next_handler

    @abstractmethod
    def handle(self, request: ExpenseRequest) -> ExpenseResponse:
        pass
