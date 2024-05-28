from responses.response import Response

from copy import deepcopy
from typing import Any, Dict, List


class ValidatedPaymentResponse(Response):

    __MANDATORY_ATTRIBUTES: List[str] = ['is_payment_valid']

    def __init__(self, response_payload: Dict[str, Any]) -> None:
        super().__init__(response_payload=response_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
