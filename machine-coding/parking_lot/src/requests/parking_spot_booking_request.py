from typing import Any, Dict, List

from .request import Request


class ParkingSpotBookingRequest(Request):

    __mandatory_attributes: List[str] = ['parking_spot', 'vehicle']

    def __init__(self, payload: Dict[str, Any]) -> None:
        super().validate_request_payload(payload=payload, mandatory_attributes=self.__class__.__mandatory_attributes)
        super().__init__(payload=payload)
