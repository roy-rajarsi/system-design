from exceptions.attribute_missing_in_request_payload_exception import AttributeMissingInRequestPayloadException

from abc import ABC, abstractmethod
from typing import Any, Dict, Final, List, Optional


class Request(ABC):

    def __init__(self, request_payload: Dict[str, Any], mandatory_attributes: List[str]) -> None:
        self.__mandatory_attributes: List[str] = mandatory_attributes
        self.__request_payload: Final[Dict[str, Any]] = request_payload
        self.__validate_request()

    def get_request_attribute(self, attribute: str) -> Optional[Any]:
        return self.__request_payload.get(attribute, None)

    def get_request_payload(self) -> Dict[str, Any]:
        return self.__request_payload

    @classmethod
    @abstractmethod
    def get_mandatory_attributes(cls) -> List[str]:
        pass

    def __validate_request(self) -> None:
        attribute: str
        for attribute in self.__mandatory_attributes:
            if self.__request_payload.get(attribute, None) is None:
                raise AttributeMissingInRequestPayloadException(request_payload=self.__request_payload, attribute_name=attribute)

    def __repr__(self) -> str:
        return f'Request({self.__request_payload})'
