from expense.models import Expense
from expense.model_validators import ExpenseValidator
from expense_handler import ExpenseHandler
from expense.expense_requests import SaveExpenseRequest
from expense.expense_responses import SaveExpenseResponse
from expense.services.money import Money
from group.models import Group, GroupToMoneyOwedInGroupIdMapping, MoneyOwedInGroupMap
from mongodb_odm.mongodbdocument import MongoDbDocument

from django.db import transaction
from django.contrib.auth.models import User
from typing import List, override


class SaveExpenseHandler(ExpenseHandler):

    def __init__(self) -> None:
        super().__init__()

    @override
    def handle(self, save_expense_request: SaveExpenseRequest) -> SaveExpenseResponse:
        expense_description: str = save_expense_request.get_request_as_dict().get('expense_description')
        payor_user: User = save_expense_request.get_request_as_dict().get('payor_user')
        debtor_list: List[User] = save_expense_request.get_request_as_dict().get('debtor_list')
        expense_distribution_list: List[Money] = save_expense_request.get_request_as_dict().get('expense_distribution_list')
        expense_type: str = save_expense_request.get_request_as_dict().get('expense_type')
        group: Group = save_expense_request.get_request_as_dict().get('group')
        expense_distribution_strategy: str = save_expense_request.get_request_as_dict().get('expense_distribution_strategy')

        index_: int
        debtor_user: User

        with transaction.atomic():
            for index_, debtor_user in enumerate(debtor_list):
                Expense(expense_description=expense_description,
                        payor_user=payor_user,
                        debtor_user=debtor_user,
                        expense_amount=expense_distribution_list[index_].get_amount(),
                        expense_currency=expense_distribution_list[index_].get_currency(),
                        expense_type=expense_type,
                        group=group,
                        expense_distribution_strategy=expense_distribution_strategy
                        ).save()

            if len(GroupToMoneyOwedInGroupIdMapping.objects.filter(group=group)) == 0:
                GroupToMoneyOwedInGroupIdMapping(group=group).save()

        if expense_type == ExpenseValidator.ExpenseType.EXPENSE_TYPE_GROUP_EXPENSE:
            MoneyOwedInGroupMap().save_document(document=MongoDbDocument(data={
                'id': list(GroupToMoneyOwedInGroupIdMapping.objects.filter(group=group))[0].id,
                'payor_user_id': payor_user.id,
                'debtor_user_list': [debtor_user.id for debtor_user in debtor_list],
                'expense_distribution_list': expense_distribution_list,
            }))

        return SaveExpenseResponse(response={'status': 'Expense Saved',
                                             'next_handler_request_payload': {
                                                 'money_owed_in_group_map_id': list(GroupToMoneyOwedInGroupIdMapping.objects.filter(group=group))[0].id
                                             }})
