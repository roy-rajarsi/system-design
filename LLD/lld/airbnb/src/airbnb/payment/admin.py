from .models import Payment

from django.contrib import admin
from typing import List


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display: List[str] = ['order_id',
                               'payment_id',
                               'payment_signature',
                               'amount',
                               'amount_paid',
                               'amount_due',
                               'currency',
                               'order_status',
                               'created_at',
                               'user',
                               'listing']
