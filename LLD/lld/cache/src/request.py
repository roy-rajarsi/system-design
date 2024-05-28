from copy import deepcopy
from typing import Any, Dict


class Request:

    __REQUEST_COUNT: int = 0

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.__request_id: int = self.__class__.__REQUEST_COUNT + 1
        self.__class__.__REQUEST_COUNT += 1
        self.__payload: Dict[str, Any] = payload

    def get_request_id(self) -> int:
        return self.__request_id

    def get_payload(self) -> Dict[str, Any]:
        return deepcopy(self.__payload)

    def __repr__(self) -> str:
        return f'Request(RequestId: {self.get_request_id()} Payload: {self.get_payload()})'
