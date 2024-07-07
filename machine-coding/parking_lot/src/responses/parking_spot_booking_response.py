from typing import Any, Dict, List

from .response import Response


class ParkingSpotBookingResponse(Response):

    __mandatory_attributes: List[str] = ['ticket_id']

    def __init__(self, payload: Dict[str, Any]) -> None:
        super().validate_response_payload(payload=payload, mandatory_attributes=self.__class__.__mandatory_attributes)
        super().__init__(payload=payload)
