from handlers.handler import Handler
from listing.models import Listing
from booking.models import Booking
from payment.models import Payment
from requests.booking.validated_payment_request import ValidatedPaymentRequest
from responses.booking.book_listing_response import BookListingResponse

from django.db import transaction
from datetime import datetime, timedelta


class BookListingHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: ValidatedPaymentRequest) -> BookListingResponse:
        booking: Booking = self.book_listing(listing_id=request.get_request_attribute(attribute='listing_id'),
                                             payment_order_id=request.get_request_attribute(attribute='order_id'),
                                             payment_id=request.get_request_attribute(attribute='payment_id'),
                                             payment_signature=request.get_request_attribute(attribute='payment_signature'),
                                             booking_start_datetime=request.get_request_attribute(attribute='booking_start_datetime'),
                                             booking_duration=timedelta(days=request.get_request_attribute('booking_duration')))
        return BookListingResponse(response_payload={
            'booking_id': booking.booking_id,
            'property': booking.listing.property.property_id,
            'booking_status': booking.booking_status
        })

    @transaction.atomic
    def book_listing(self, listing_id: int, payment_order_id: str, payment_id: str, payment_signature: str, booking_start_datetime: datetime, booking_duration: timedelta) -> Booking:
        listing: Listing = Listing.objects.select_for_update().get(id=listing_id)
        payment: Payment = Payment.objects.select_for_update().get(order_id=payment_order_id)
        listing.available_from = booking_start_datetime + booking_duration  # Very subtle way of doing this, although not correct
        listing.save()
        payment.payment_id = payment_id
        payment.payment_signature = payment_signature
        payment.amount_due = 0
        payment.amount_paid = payment.amount
        payment.order_status = 'paid'
        payment.save()
        booking: Booking = Booking(listing=listing,
                                   payment=payment,
                                   booking_start_datetime=booking_start_datetime,
                                   booking_duration_in_days=booking_duration.days,
                                   booking_end_datetime=booking_start_datetime+booking_duration,
                                   booking_status='BOOKED')
        booking.save()
        return booking
