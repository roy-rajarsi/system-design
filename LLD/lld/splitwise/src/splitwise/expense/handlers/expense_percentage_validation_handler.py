from expense_handler import ExpenseHandler
from expense.expense_requests import ExpensePercentageValidationRequest
from expense.expense_responses import ExpensePercentageValidationResponse

from typing import override


class ExpensePercentageValidationHandler(ExpenseHandler):

    def __init__(self) -> None:
        super().__init__()

    @override
    def handle(self, expense_percentage_validation_request: ExpensePercentageValidationRequest) -> ExpensePercentageValidationResponse:

        sum_of_percentages: int = 0

        user_id: int
        for user_id in expense_percentage_validation_request.get_request_as_dict().get('expense_percentage_map'):
            sum_of_percentages += expense_percentage_validation_request.get_request_as_dict().get('expense_percentage_map').get(user_id)

        return ExpensePercentageValidationResponse(response={'is_valid_expense_percentage_distribution': sum_of_percentages == 100})
