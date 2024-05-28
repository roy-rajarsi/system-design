from model_validators import ExpenseValidator, GroupExpenseValidator
from group.models import Group

from django.contrib.auth.models import User
from django.db import models


class Expense(models.Model):
    id: models.AutoField = models.AutoField(primarykey=True)
    expense_description: models.CharField = models.CharField(max_length=150, blank=True)
    payor_user: models.ForeignKey = models.ForeignKey(to=User, on_delete=models.CASCADE)
    debtor_user: models.ForeignKey = models.ForeignKey(to=User, on_delete=models.CASCADE)
    expense_amount: models.DecimalField = models.DecimalField(decimal_places=5)
    expense_currency: models.CharField = models.CharField(max_length=12, validators=[ExpenseValidator.is_expense_currency_valid])
    expense_type: models.CharField(max_length=30, validators=[ExpenseValidator.is_expense_type_valid])
    group: models.ForeignKey = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True)
    expense_distribution_strategy = models.CharField(max_length=46, validators=[GroupExpenseValidator.is_money_distribution_strategy_valid])

    def __repr__(self) -> str:
        return f'Expense(id: {self.id} payor: {self.payor_user} debtor: {self.debtor_user} expense_money: {self.expense_amount} {self.expense_currency})'
