from .models import Payment

from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from typing import List


class PaymentSerializer(ModelSerializer):

    class Meta:
        model: Model = Payment
        fields: List[str] = '__all__'
