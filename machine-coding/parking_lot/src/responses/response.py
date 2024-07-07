from abc import ABC
from typing import Any, Dict, Final, List
from uuid import UUID, uuid4

from exceptions.validation_error import ValidationError


class Response(ABC):

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.__id: Final[UUID] = uuid4()
        self.__payload: Final[Dict[str, Any]] = payload

    def get_id(self) -> UUID:
        return self.__id

    def get_payload(self) -> Dict[str, Any]:
        return self.__payload

    @staticmethod
    def validate_response_payload(payload: Dict[str, Any], mandatory_attributes: List[str]) -> None:
        attribute: str
        for attribute in mandatory_attributes:
            if attribute not in payload:
                raise ValidationError(attribute=attribute, payload=payload)
