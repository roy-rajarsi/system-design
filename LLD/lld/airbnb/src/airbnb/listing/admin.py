from .models import Listing

from django.contrib.admin import ModelAdmin, register
from typing import List


@register(Listing)
class ListingAdmin(ModelAdmin):
    list_display: List[str] = ['id', 'state', 'city', 'region', 'property', 'available_from', 'price', 'is_available_for_booking']
