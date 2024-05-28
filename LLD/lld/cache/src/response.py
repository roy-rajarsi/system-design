from copy import deepcopy
from typing import Any, Dict


class Response:
    __RESPONSE_COUNT: int = 0

    def __init__(self, payload: Dict[str, Any], status_code: str = 'HTTP_200_OK') -> None:
        self.__response_id: int = self.__class__.__RESPONSE_COUNT + 1
        self.__class__.__RESPONSE_COUNT += 1
        self.__payload: Dict[str, Any] = payload
        self.__status_code: str = status_code

    def get_response_id(self) -> int:
        return self.__response_id

    def get_payload(self) -> Dict[str, Any]:
        return deepcopy(self.__payload)

    def get_status_code(self) -> str:
        return self.__status_code

    def __repr__(self) -> str:
        return f'Response(ResponseId: {self.get_response_id()} Payload: {self.get_payload()} StatusCode: {self.get_status_code()})'
