from exceptions.attribute_missing_in_request_payload_exception import AttributeMissingInRequestPayloadException

from rest_framework.request import Request
from typing import Any, Dict, List, Tuple


def generate_request_payload_from_request(request: Request, mandatory_attributes: List[str]) -> Dict[str, Any]:
    request_payload: Dict[str, Any] = dict()

    attribute: str
    for attribute in mandatory_attributes:
        if request.data.get(attribute, None) is None:
            raise AttributeMissingInRequestPayloadException(request=request, attribute_name=attribute)
        request_payload[attribute] = request.data.get(attribute)

    return request_payload


def get_normalised_coordinates(coordinates: Tuple[float, float]) -> Tuple[float, float]:
    normalised_latitude: float = coordinates[0] + 90
    normalised_longitude: float = coordinates[1] + 180
    return normalised_latitude, normalised_longitude
