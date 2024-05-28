from listing.models import Listing
from payment.models import Payment

from django.core.validators import MinValueValidator
from django.db import models


class Booking(models.Model):

    class BookingStatus(models.TextChoices):
        BOOKED = 'BOOKED', 'BOOKED'
        EXPIRED = 'EXPIRED', 'BOOKING_EXPIRED'

    booking_id: models.AutoField = models.AutoField(primary_key=True)
    listing: models.ForeignKey = models.ForeignKey(to=Listing, on_delete=models.CASCADE, related_name='booking_listing')
    payment: models.ForeignKey = models.ForeignKey(to=Payment, on_delete=models.CASCADE, related_name='booking_payment')
    booking_start_datetime: models.DateTimeField = models.DateTimeField()
    booking_duration_in_days: models.IntegerField = models.IntegerField(MinValueValidator(limit_value=1))
    booking_end_datetime: models.DateTimeField = models.DateTimeField()
    booking_status: models.CharField = models.CharField(max_length=20, choices=BookingStatus)

    def __repr__(self) -> str:
        return f'Booking(BookingId: {self.id} ListingId: {self.listing} PaymentId: {self.payment})'
