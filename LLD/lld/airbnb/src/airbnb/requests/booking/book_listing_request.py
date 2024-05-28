from requests.request import Request

from copy import deepcopy
from typing import Any, Dict, List


class BookListingRequest(Request):

    __MANDATORY_ATTRIBUTES: List[str] = ['listing_id', 'order_id', 'payment_id', 'payment_signature', 'booking_duration']

    def __init__(self, request_payload: Dict[str, Any]) -> None:
        super().__init__(request_payload=request_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
