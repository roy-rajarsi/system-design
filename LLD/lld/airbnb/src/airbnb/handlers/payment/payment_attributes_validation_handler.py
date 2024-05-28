from exceptions.payment.payment_attributes_invalid_exception import PaymentAttributesInvalidException
from handlers.handler import Handler
from payment.models import Payment
from requests.payment.payment_initiation_request import PaymentInitiationRequest
from responses.payment.payment_attributes_validated_response import PaymentAttributesValidatedResponse


class PaymentAttributesValidationHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: PaymentInitiationRequest) -> PaymentAttributesValidatedResponse:
        if request.get_request_attribute(attribute='amount') < 0:
            raise PaymentAttributesInvalidException(attribute_name='amount',
                                                    attribute_value=request.get_request_attribute(attribute='amount'))
        if request.get_request_attribute(attribute='amount') != request.get_request_attribute(attribute='listing').price:
            raise PaymentAttributesInvalidException(attribute_name='amount',
                                                    attribute_value=request.get_request_attribute(attribute='amount'),
                                                    listing_price=request.get_request_attribute('listing').price)
        if request.get_request_attribute(attribute='currency') not in [choice[0] for choice in Payment.Currency.choices]:
            raise PaymentAttributesInvalidException(attribute_name='currency',
                                                    attribute_value=request.get_request_attribute(attribute='currency'),
                                                    valid_values=[choice[0] for choice in Payment.Currency.choices])
        return PaymentAttributesValidatedResponse(response_payload={
            ** request.get_request_payload(),
            'is_payment_attributes_validated': True
        })
