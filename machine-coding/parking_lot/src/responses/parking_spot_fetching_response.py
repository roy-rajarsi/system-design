from typing import Any, Dict, List

from .response import Response


class ParkingSpotFetchingResponse(Response):

    __mandatory_attributes: List[str] = ['parking_spot']

    def __init__(self, payload: Dict[str, Any]) -> None:
        super().validate_response_payload(payload=payload, mandatory_attributes=self.__class__.__mandatory_attributes)
        super().__init__(payload=payload)

