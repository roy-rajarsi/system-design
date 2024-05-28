from .models import Property

from django.contrib.admin import ModelAdmin, register
from typing import List


@register(Property)
class PropertyAdmin(ModelAdmin):
    list_display: List[str] = ['property_id', 'name', 'latitude', 'longitude', 'address', 'description', 'images_url']
