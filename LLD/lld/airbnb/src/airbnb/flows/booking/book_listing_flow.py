from typing import Dict, Any

from flows.execution_flow import ExecutionFlow
from handlers.handler import Handler
from handlers.booking.payment_validation_handler import PaymentValidationHandler
from handlers.booking.book_listing_handler import BookListingHandler
from requests.request import Request
from requests.booking.book_listing_request import BookListingRequest
from requests.booking.validated_payment_request import ValidatedPaymentRequest
from requests.none_request import NoneRequest
from responses.response import Response
from responses.booking.validated_payment_response import ValidatedPaymentResponse
from responses.booking.book_listing_response import BookListingResponse
from responses.none_response import NoneResponse


class BookListingFlow(ExecutionFlow):

    def __init__(self) -> None:
        super().__init__(list_of_handlers=[
            PaymentValidationHandler(), BookListingHandler()
        ])
        self.set_chain_of_execution()

    def set_chain_of_execution(self) -> None:
        previous_handler: Handler = self.get_head_handler()
        current_handler: Handler
        index_: int
        for index_ in range(1, self.get_count_of_handlers()):
            current_handler = self.get_list_of_handlers()[index_]
            previous_handler.set_next_handler(next_handler=current_handler)
            previous_handler = current_handler

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        current_handler: Handler = self.get_head_handler()
        request: Request = self.generate_request_for_head_handler(request_payload=request)
        response: Response = NoneResponse()
        while current_handler is not None:
            print(current_handler)
            response = current_handler.handle(request=request)
            print(response, type(response))
            request = self.generate_request_for_handler(response=response)
            current_handler = current_handler.get_next_handler()
        return self.generate_response_payload_from_tail_handler(response=response)

    def generate_request_for_head_handler(self, request_payload: Dict[str, Any]) -> BookListingRequest:
        return BookListingRequest(request_payload=request_payload)

    def generate_request_for_handler(self, response: Response) -> Request:
        if isinstance(response, ValidatedPaymentResponse):
            return ValidatedPaymentRequest(request_payload={**response.get_response_payload()})
        else:
            return NoneRequest()

    def generate_response_payload_from_tail_handler(self, response: Response) -> Dict[str, Any]:
        print(response, type(response))
        assert isinstance(response, BookListingResponse)
        return {**response.get_response_payload()}
