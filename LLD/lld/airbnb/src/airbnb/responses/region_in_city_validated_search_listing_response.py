from .response import Response

from copy import deepcopy
from typing import Any, Dict, List


class RegionInCityValidatedSearchListingResponse(Response):
    __MANDATORY_ATTRIBUTES: List[str] = ['city', 'city_coordinates', 'region', 'region_coordinates', 'tentative_booking_date', 'price_start_range', 'price_end_range', 'is_region_in_city']

    def __init__(self, response_payload: Dict[str, Any]) -> None:
        super().__init__(response_payload=response_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
