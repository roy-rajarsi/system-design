from exceptions.attribute_missing_in_response_payload_exception import AttributeMissingInResponsePayloadException

from abc import ABC, abstractmethod
from typing import Any, Dict, Final, List, Optional


class Response(ABC):

    def __init__(self, response_payload: Dict[str, Any], mandatory_attributes: List[str]) -> None:
        self.__mandatory_attributes: List[str] = mandatory_attributes
        self.__response_payload: Final[Dict[str, Any]] = response_payload
        self.__validate_response()

    def get_response_payload(self) -> Dict[str, Any]:
        return self.__response_payload

    def get_response_attribute(self, attribute: str) -> Optional[Any]:
        return self.__response_payload.get(attribute, None)

    @classmethod
    @abstractmethod
    def get_mandatory_attributes(cls) -> List[str]:
        pass

    def __validate_response(self) -> None:
        attribute: str
        for attribute in self.__mandatory_attributes:
            if self.__response_payload.get(attribute, None) is None:
                raise AttributeMissingInResponsePayloadException(response_payload=self.__response_payload, attribute_name=attribute)

    def __repr__(self) -> str:
        return f'Response({self.__response_payload})'
