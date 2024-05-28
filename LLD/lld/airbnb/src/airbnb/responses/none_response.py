from .response import Response

from copy import deepcopy
from typing import Dict, List


class NoneResponse(Response):
    __MANDATORY_ATTRIBUTES: List[str] = list()

    def __init__(self) -> None:
        response_payload: Dict = dict()
        super().__init__(response_payload=response_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
