from .models import Listing

from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from typing import List


class ListingSerializer(ModelSerializer):
    class Meta:
        model: Model = Listing
        fields: List[str] = '__all__'

# {"state": 1, "city": 1, "property": 1, "price": 1}
