from listing.models import Listing

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from typing import List


class Payment(models.Model):

    class Currency(models.TextChoices):
        INR = 'INR', 'INR'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        MXN = 'MXN', 'MXN'
        CAD = 'CAD', 'CAD'

    class OrderStatus(models.TextChoices):
        created = 'created', 'created'
        attempted = 'attempted', 'attempted'
        paid = 'paid', 'paid'

    # The attributes "order_id" to "created_at" are the primary data kv pairs returned after calling the Razorpay Api
    order_id: models.CharField = models.CharField(max_length=25, primary_key=True)
    payment_id: models.CharField = models.CharField(max_length=50, blank=True)  # payment_id will be populated after successful payment from frontend
    payment_signature: models.CharField = models.CharField(max_length=100, blank=True)  # payment_signature will be populated after successful payment from frontend
    amount: models.FloatField = models.FloatField(validators=[MinValueValidator(limit_value=0)])
    amount_paid: models.FloatField = models.FloatField(validators=[MinValueValidator(limit_value=0)])
    amount_due: models.FloatField = models.FloatField(validators=[MinValueValidator(limit_value=0)])
    currency: models.CharField = models.CharField(max_length=3, choices=Currency)
    order_status: models.CharField = models.CharField(max_length=9, choices=OrderStatus)
    created_at: models.DateTimeField = models.DateTimeField()
    user: models.ForeignKey = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='payment_user')
    listing: models.ForeignKey = models.ForeignKey(to=Listing, on_delete=models.CASCADE, related_name='payment_listing')

    @classmethod
    def get_list_of_valid_currencies(cls) -> List[str]:
        print(cls.Currency.choices)
        return cls.Currency.choices

    def __repr__(self) -> str:
        return f'Payment(OrderId: {self.order_id} Amount: {self.amount} Currency: {self.currency} OrderStatus -> {self.order_status})'
