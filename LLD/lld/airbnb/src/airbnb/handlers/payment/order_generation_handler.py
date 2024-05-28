from handlers.handler import Handler
from listing.models import Listing
from payment.models import Payment
from payment.serializers import PaymentSerializer
from requests.payment.order_generation_request import OrderGenerationRequest
from responses.payment.payment_initiation_response import PaymentInitiationResponse

from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.db import DatabaseError
from django.utils.crypto import get_random_string
from logging import Logger, getLogger, INFO, ERROR
from time import sleep
from typing import Any, Dict


logger: Logger = getLogger(name=__name__)


class OrderGenerationHandler(Handler):

    def handle(self, request: OrderGenerationRequest) -> PaymentInitiationResponse:
        response_payload: Dict[str, Any]
        try:
            order_id: str = self.generate_order(user=request.get_request_attribute(attribute='user'),
                                                listing=request.get_request_attribute(attribute='listing'),
                                                amount=request.get_request_attribute(attribute='amount'),
                                                currency=request.get_request_attribute(attribute='currency'))
            response_payload = {**PaymentSerializer(Payment.objects.get(order_id=order_id)).data}
            return PaymentInitiationResponse(response_payload=response_payload)
        except ValidationError as validation_error:
            logger.log(level=ERROR, msg=f'ValidationError Occurred -> {validation_error}', exc_info=True)
            raise validation_error
        except DatabaseError as database_error:
            logger.log(level=ERROR, msg=f'Database Object is Locked by a different thread -> {database_error}', exc_info=True)
            raise database_error
        except Exception as exception:
            logger.log(level=ERROR, msg=f'Exception Occurred -> {exception}', exc_info=True)
            raise exception

    @transaction.atomic()
    def generate_order(self, user: User, listing: Listing, amount: float, currency: Payment.Currency) -> str:
        # with transaction.atomic():
        listing: Listing = Listing.objects.select_for_update(nowait=False).get(id=listing.id)

        # Request the Payment Gateway to create an order and get the Order response.
        # 1s sleep is a simulation of the latency introduced due to the Payment Gateway (Razorpay) api call
        sleep(1)
        order: Dict[str, Any] = {
            'order_id': get_random_string(length=25,
                                          allowed_chars=OrderGenerationHandler.generate_allowed_characters()),
            'amount': amount,
            'amount_paid': 0,
            'amount_due': amount,
            'currency': currency,
            'order_status': 'created',
            'created_at': datetime.now(),
        }
        # Response received and stored in the dictionary named order

        payment_serializer: PaymentSerializer = PaymentSerializer(data={
            **order,
            'user': user.id,
            'listing': listing.id
        })
        if payment_serializer.is_valid(raise_exception=True):
            payment_serializer.save()

        listing.is_available_for_booking = False
        listing.save()

        logger.log(level=INFO, msg=f'Queries executed:: {connection.queries}')
        return order.get('order_id')

    @staticmethod
    def generate_allowed_characters() -> str:
        capital_alphabets: str = ''.join([chr(ascii_) for ascii_ in range(65, 91)])
        small_alphabets: str = ''.join([chr(ascii_) for ascii_ in range(97, 123)])
        digits: str = ''.join([str(digit) for digit in range(0, 10)])
        special_characters: str = '!@#$%^&*()_-+=|/?<>.,`~'

        allowed_characters: str = ''.join([
            capital_alphabets,
            small_alphabets,
            digits,
            special_characters
        ])
        return allowed_characters
