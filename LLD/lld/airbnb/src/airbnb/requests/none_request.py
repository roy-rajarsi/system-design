from .request import Request

from copy import deepcopy
from typing import Any, Dict, List


class NoneRequest(Request):

    __MANDATORY_ATTRIBUTES: List[str] = list()

    def __init__(self) -> None:
        request_payload: Dict[str, Any] = dict()
        super().__init__(request_payload=request_payload, mandatory_attributes=self.__class__.__MANDATORY_ATTRIBUTES)

    @classmethod
    def get_mandatory_attributes(cls) -> List[str]:
        return deepcopy(cls.__MANDATORY_ATTRIBUTES)
