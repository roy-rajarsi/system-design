from .models import Property

from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from typing import List


class PropertySerializer(ModelSerializer):

    class Meta:
        model: Model = Property
        fields: List[str] = '__all__'
