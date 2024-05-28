from .models import Booking

from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from typing import List


class BookingSerializer(ModelSerializer):

    class Meta:
        model: Model = Booking
        fields: List[str] = '__all__'
