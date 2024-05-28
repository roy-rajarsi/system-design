from geo.models import City, Region, State
from property.models import Property

from django.db import models
from django.core.validators import MinValueValidator
from typing import List


class Listing(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    state: models.ForeignKey = models.ForeignKey(to=State, on_delete=models.CASCADE, related_name='state')
    city: models.ForeignKey = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='listing_city')
    region: models.ForeignKey = models.ForeignKey(to=Region, on_delete=models.CASCADE, related_name='listing_region')
    property: models.ForeignKey = models.ForeignKey(to=Property, on_delete=models.CASCADE, related_name='property')
    available_from: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    price: models.FloatField = models.FloatField(validators=[MinValueValidator(0)])
    is_available_for_booking: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        indexes: List[models.Index] = [models.Index(fields=['state', 'city', 'region', 'available_from', 'price'])]

    def __repr__(self) -> str:
        return f'Listing(Id: {self.id} Property: {self.property} Price: {self.price} AvailableFrom: {self.available_from})'
