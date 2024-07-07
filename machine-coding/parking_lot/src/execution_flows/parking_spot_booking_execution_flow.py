from typing import Any, Dict, Optional

from .execution_flow import ExecutionFlow
from handlers.handler import Handler
from handlers.parking_spot_fetching_handler import ParkingSpotFetchingHandler
from handlers.parking_spot_booking_handler import ParkingSpotBookingHandler
from requests.request import Request
from requests.parking_spot_fetching_request import ParkingSpotFetchingRequest
from requests.parking_spot_booking_request import ParkingSpotBookingRequest
from requests.none_request import NoneRequest
from responses.response import Response
from responses.parking_spot_fetching_response import ParkingSpotFetchingResponse
from responses.parking_spot_booking_response import ParkingSpotBookingResponse
from responses.none_response import NoneResponse


class ParkingSpotBookingExecutionFlow(ExecutionFlow):

    def __init__(self) -> None:
        super().__init__(handlers=[ParkingSpotFetchingHandler(), ParkingSpotBookingHandler()])
        self.define_chain_of_responsibility()

    def define_chain_of_responsibility(self) -> None:
        previous_handler: Handler = self.get_head_handler()
        current_handler: Handler
        index_: int
        for index_, current_handler in enumerate(self.__handlers):
            if index_ != 0:
                previous_handler.set_next_handler(next_handler=current_handler)
                previous_handler = current_handler

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        current_handler: Optional[Handler] = self.get_head_handler()
        request_payload: Dict[str, Any] = request
        request: Request
        response: Response = NoneResponse()
        while current_handler is not None:
            if current_handler == self.get_head_handler():
                request = ParkingSpotFetchingRequest(payload=request_payload)
            else:
                request = ParkingSpotBookingExecutionFlow.__generate_request_from_response(response=response)
            response = current_handler.handle(request=request)

        parking_spot_booking_response: ParkingSpotBookingResponse = response
        return parking_spot_booking_response.get_payload()

    @staticmethod
    def __generate_request_from_response(response: Response) -> Request:
        if isinstance(response, ParkingSpotFetchingResponse):
            return ParkingSpotBookingRequest(payload=response.get_payload())
        else:
            return NoneRequest()
