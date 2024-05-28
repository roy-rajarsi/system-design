# Generated by Django 5.0.6 on 2024-05-15 11:30

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField(editable=False, unique=True, validators=[django.core.validators.MinValueValidator(limit_value=-90), django.core.validators.MaxValueValidator(limit_value=90)])),
                ('longitude', models.FloatField(editable=False, unique=True, validators=[django.core.validators.MinValueValidator(limit_value=-180), django.core.validators.MaxValueValidator(limit_value=180)])),
                ('mean_length_in_kms', models.FloatField(editable=False, validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=150)])),
                ('mean_breadth_in_kms', models.FloatField(editable=False, validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=150)])),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='geo.city')),
            ],
        ),
    ]
