from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Property(models.Model):
    property_id: models.AutoField = models.AutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    latitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-90), MaxValueValidator(limit_value=90)])
    longitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-180), MaxValueValidator(limit_value=180)])
    address: models.CharField = models.CharField(max_length=200)
    description: models.CharField = models.CharField(max_length=500)
    images_url: models.URLField = models.URLField(max_length=500, default=str())

    def __repr__(self) -> str:
        return f'Property(Id: {self.property_id} Name: {self.name} Coordinates: (Latitude={self.latitude}, Longitude={self.longitude}))'
