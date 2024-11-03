from typing import Any, Dict, Final, override
from uuid import UUID, uuid4

from enums.http_status import HttpStatus


class Response:

    def __init__(self, payload: Dict[str, Any], status: HttpStatus) -> None:
        self.__response_id: Final[UUID] = uuid4()
        self.__payload: Final[Dict[str, Any]] = payload
        self.__status: HttpStatus = status

    def get_response_id(self) -> UUID:
        return self.__response_id

    def get_payload(self) -> Dict[str, Any]:
        return self.__payload

    def get_status(self) -> HttpStatus:
        return self.__status

    @override
    def __repr__(self) -> str:
        return f'Response(Id: {self.__response_id} \nPayload: {self.__payload} \nStatus: {self.__status})'
