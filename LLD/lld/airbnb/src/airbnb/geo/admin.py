from .models import City, Region, State

from django.contrib.admin import ModelAdmin, register
from typing import List


@register(City)
class CityAdmin(ModelAdmin):
    list_display: List[str] = ['id', 'name', 'latitude', 'longitude', 'mean_length_in_kms', 'mean_breadth_in_kms']


@register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ['id', 'name', 'city', 'latitude', 'longitude']


@register(State)
class StateAdmin(ModelAdmin):
    list_display: List[str] = ['id', 'name', 'city']
