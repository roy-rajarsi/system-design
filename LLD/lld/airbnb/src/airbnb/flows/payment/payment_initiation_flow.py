from flows.execution_flow import ExecutionFlow
from handlers.handler import Handler
from handlers.payment.payment_attributes_validation_handler import PaymentAttributesValidationHandler
from handlers.payment.order_generation_handler import OrderGenerationHandler
from requests.payment.payment_initiation_request import PaymentInitiationRequest
from requests.payment.order_generation_request import OrderGenerationRequest
from requests.request import Request
from requests.none_request import NoneRequest
from responses.payment.payment_attributes_validated_response import PaymentAttributesValidatedResponse
from responses.payment.payment_initiation_response import PaymentInitiationResponse
from responses.response import Response
from responses.none_response import NoneResponse

from logging import Logger, getLogger, WARNING
from typing import Any, Dict


logger: Logger = getLogger(name=__name__)


class PaymentInitiationFlow(ExecutionFlow):

    def __init__(self) -> None:
        super().__init__(list_of_handlers=[
            PaymentAttributesValidationHandler(), OrderGenerationHandler()
        ])
        self.set_chain_of_execution()

    def set_chain_of_execution(self) -> None:
        previous_handler: Handler = self.get_head_handler()
        count_of_handlers: int = self.get_count_of_handlers()
        print(self.get_list_of_handlers())
        index_: int
        for index_ in range(1, count_of_handlers):
            current_handler: Handler = self.get_list_of_handlers()[index_]
            previous_handler.set_next_handler(next_handler=current_handler)
            previous_handler = current_handler

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        request: Request = self.generate_request_for_head_handler(request_payload=request)
        current_handler: Handler = self.get_head_handler()
        response: Response = NoneResponse()
        while current_handler is not None:
            response: Response = current_handler.handle(request=request)
            current_handler = current_handler.get_next_handler()
            request = self.generate_request_for_handler(response=response)
        return self.generate_response_payload_from_tail_handler(response=response)

    def generate_request_for_head_handler(self, request_payload: Dict[str, Any]) -> PaymentInitiationRequest:
        return PaymentInitiationRequest(request_payload=request_payload)

    def generate_request_for_handler(self, response: Response) -> Request:
        if isinstance(response, PaymentAttributesValidatedResponse):
            return OrderGenerationRequest(request_payload={**response.get_response_payload()})
        else:
            logger.log(level=WARNING, msg=f'NoneRequest Instance returned for response -> {response}')
            return NoneRequest()

    def generate_response_payload_from_tail_handler(self, response: Response) -> Dict[str, Any]:
        assert isinstance(response, PaymentInitiationResponse)
        return response.get_response_payload()
