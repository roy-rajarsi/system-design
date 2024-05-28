from expense_handler import ExpenseHandler
from expense.expense_requests import PayorDebtorExpenseRelationshipGenerationRequest
from expense.expense_responses import PayorDebtorExpenseRelationshipGenerationResponse
from expense.model_validators import ExpenseValidator
from expense.strategies.group_expense_distribution_strategies.group_expense_distribution_strategies import GroupExpenseDistributionStrategies
from expense.strategies.group_expense_distribution_strategies.group_expense_distribution_strategy_equal_distribution import GroupExpenseDistributionStrategyEqualDistribution
from expense.strategies.group_expense_distribution_strategies.group_expense_distribution_strategy_percentage_distribution import GroupExpenseDistributionStrategyPercentageDistribution
from expense.services.money import Money

from decimal import Decimal
from typing import Dict, List, override


class PayorDebtorExpenseRelationshipGenerationHandler(ExpenseHandler):

    def __init__(self) -> None:
        super().__init__()

    @override
    def handle(self, payor_debtor_expense_relationship_generation_request: PayorDebtorExpenseRelationshipGenerationRequest) -> PayorDebtorExpenseRelationshipGenerationResponse:

        if payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense_type') == ExpenseValidator.ExpenseType.EXPENSE_TYPE_GROUP_EXPENSE:
            return PayorDebtorExpenseRelationshipGenerationHandler.__generate_payor_debtor_expense_relationship_for_group_expense(payor_debtor_expense_relationship_generation_request=payor_debtor_expense_relationship_generation_request)
        elif payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense_type') == ExpenseValidator.ExpenseType.EXPENSE_TYPE_NON_GROUP_EXPENSE:
            return PayorDebtorExpenseRelationshipGenerationHandler.__generate_payor_debtor_expense_relationship_for_non_group_expense(payor_debtor_expense_relationship_generation_request=payor_debtor_expense_relationship_generation_request)

    @staticmethod
    def __generate_payor_debtor_expense_relationship_for_group_expense(payor_debtor_expense_relationship_generation_request: PayorDebtorExpenseRelationshipGenerationRequest) -> PayorDebtorExpenseRelationshipGenerationResponse:

        if payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense_distribution_type') == GroupExpenseDistributionStrategies.GROUP_EXPENSE_DISTRIBUTION_STRATEGY_EQUAL:
            debtor_list: List[int] = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('debtor_list')
            expense: Money = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense')
            payor_debtor_expense_relationship_map: Dict[int, Money] = GroupExpenseDistributionStrategyEqualDistribution().generate_debtor_user_id_to_money_owed_map(debtor_list=debtor_list, expense=expense)
            payor_debtor_expense_relationship_generation_response: PayorDebtorExpenseRelationshipGenerationResponse = PayorDebtorExpenseRelationshipGenerationResponse(response={
                                                                                                                                                                                    'payor_debtor_expense_relationship': payor_debtor_expense_relationship_map
                                                                                                                                                                                })

        # elif payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense_distribution_type') == GroupExpenseDistributionStrategies.GROUP_EXPENSE_DISTRIBUTION_STRATEGY_PERCENTAGE:
        else:
            debtor_list: List[int] = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('debtor_list')
            expense: Money = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense')
            expense_distribution_percentage_list: List[Decimal] = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense_distribution_percentage_list')
            payor_debtor_expense_relationship_map: Dict[int, Money] = GroupExpenseDistributionStrategyPercentageDistribution().generate_debtor_user_id_to_money_owed_map(debtor_list=debtor_list, expense=expense, expense_distribution_percentage_list=expense_distribution_percentage_list)
            payor_debtor_expense_relationship_generation_response: PayorDebtorExpenseRelationshipGenerationResponse = PayorDebtorExpenseRelationshipGenerationResponse(response={
                                                                                                                                                                                    'payor_debtor_expense_relationship': payor_debtor_expense_relationship_map
                                                                                                                                                                                })
        return payor_debtor_expense_relationship_generation_response

    @staticmethod
    def __generate_payor_debtor_expense_relationship_for_non_group_expense(payor_debtor_expense_relationship_generation_request: PayorDebtorExpenseRelationshipGenerationRequest) -> PayorDebtorExpenseRelationshipGenerationResponse:
        debtor_list: List[int] = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('debtor_list')
        expense: Money = payor_debtor_expense_relationship_generation_request.get_request_as_dict().get('expense')
        payor_debtor_expense_relationship_map: Dict[int, Money] = GroupExpenseDistributionStrategyEqualDistribution().generate_debtor_user_id_to_money_owed_map(debtor_list=debtor_list, expense=expense)
        payor_debtor_expense_relationship_generation_response: PayorDebtorExpenseRelationshipGenerationResponse = PayorDebtorExpenseRelationshipGenerationResponse(response={
                                                                                                                                                                                'payor_debtor_expense_relationship': payor_debtor_expense_relationship_map
                                                                                                                                                                            })
        return payor_debtor_expense_relationship_generation_response
