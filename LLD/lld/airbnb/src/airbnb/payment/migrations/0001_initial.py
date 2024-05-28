# Generated by Django 5.0.6 on 2024-05-27 18:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0002_remove_listing_listing_lis_state_i_e7e3cc_idx_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('order_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('payment_id', models.CharField(blank=True, max_length=50)),
                ('payment_signature', models.CharField(blank=True, max_length=100)),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('amount_paid', models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('amount_due', models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('currency', models.CharField(choices=[('INR', 'INR'), ('USD', 'USD'), ('EUR', 'EUR'), ('MXN', 'MXN'), ('CAD', 'CAD')], max_length=3)),
                ('order_status', models.CharField(choices=[('created', 'created'), ('attempted', 'attempted'), ('paid', 'paid')], max_length=9)),
                ('created_at', models.DateTimeField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_listing', to='listing.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
