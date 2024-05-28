from .models import Booking

from django.contrib import admin
from typing import List

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display: List[str] = ['booking_id', 'listing', 'payment', 'booking_start_datetime', 'booking_duration_in_days', 'booking_end_datetime', 'booking_status']
