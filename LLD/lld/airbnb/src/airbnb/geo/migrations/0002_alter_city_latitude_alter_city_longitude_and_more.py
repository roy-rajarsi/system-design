# Generated by Django 5.0.6 on 2024-05-16 12:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.FloatField(unique=True, validators=[django.core.validators.MinValueValidator(limit_value=-90), django.core.validators.MaxValueValidator(limit_value=90)]),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.FloatField(unique=True, validators=[django.core.validators.MinValueValidator(limit_value=-180), django.core.validators.MaxValueValidator(limit_value=180)]),
        ),
        migrations.AlterField(
            model_name='city',
            name='mean_breadth_in_kms',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=150)]),
        ),
        migrations.AlterField(
            model_name='city',
            name='mean_length_in_kms',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=150)]),
        ),
    ]
