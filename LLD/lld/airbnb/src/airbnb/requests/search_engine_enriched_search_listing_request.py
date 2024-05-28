from .request import Request

from copy import deepcopy
from typing import Any, Dict, List


class SearchEngineEnrichedSearchListingRequest(Request):

    __MANDATORY_ATTRIBUTES: List[str] = ['city', 'city_coordinates', 'region', 'region_coordinates', 'tentative_booking_date', 'price_start_range', 'price_end_range', 'is_region_in_city', 'search_engine']

    def __init__(self, request_payload: Dict[str, Any]) -> None:
        super().__init__(request_payload=request_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
