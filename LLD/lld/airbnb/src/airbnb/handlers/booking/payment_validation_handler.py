from handlers.handler import Handler
from payment.models import Payment
from requests.booking.book_listing_request import BookListingRequest
from responses.booking.validated_payment_response import ValidatedPaymentResponse

from logging import Logger, getLogger, ERROR


logger: Logger = getLogger(name=__name__)


class PaymentValidationHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: BookListingRequest) -> ValidatedPaymentResponse:
        try:
            is_payment_valid: bool = False
            payment: Payment = Payment.objects.get(order_id=request.get_request_attribute(attribute='order_id'))

            # Razorpay Api Call to verify payment using order_id, payment_id and payment_signature

            return ValidatedPaymentResponse(response_payload={
                ** request.get_request_payload(),
                'is_payment_valid': is_payment_valid
            })

        # Throwing a generic exception, as we may have various types of exceptions, depending on the Payment Gateway we are integrating with
        except Exception as exception:
            logger.log(level=ERROR, msg=f'Exception Occurred: {str(exception)}', exc_info=True)
            raise exception
