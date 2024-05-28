from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class City(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    latitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-90), MaxValueValidator(limit_value=90)])
    longitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-180), MaxValueValidator(limit_value=180)])
    mean_length_in_kms: models.FloatField = models.FloatField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=150)])
    mean_breadth_in_kms: models.FloatField = models.FloatField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=150)])

    def __repr__(self) -> str:
        return f'City(Id: {self.id} Name: {self.name})'


class Region(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    city: models.ForeignKey = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='city_of_region')
    latitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-90), MaxValueValidator(limit_value=90)])
    longitude: models.FloatField = models.FloatField(unique=True, validators=[MinValueValidator(limit_value=-180), MaxValueValidator(limit_value=180)])

    def __repr__(self) -> str:
        return f'Region(Id: {self.id} Name: {self.name} City: {self.city})'


class State(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    city: models.ForeignKey = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='city')

    def __repr__(self) -> str:
        return f'State(Id: {self.id}, Name: {self.name})'
