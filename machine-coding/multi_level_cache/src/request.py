from typing import Any, Dict, Final, override
from uuid import uuid4, UUID


class Request:

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.__request_id: Final[UUID] = uuid4()
        self.__payload: Final[Dict[str, Any]] = payload

    def get_request_id(self) -> UUID:
        return self.__request_id

    def get_payload(self) -> Dict[str, Any]:
        return self.__payload

    @override
    def __repr__(self) -> str:
        return f'Request(Id: {self.__request_id} \nPayload: {self.__payload})'
