from typing import Any, Dict


class AttributeMissingInRequestPayloadException(Exception):

    def __init__(self, request_payload: Dict[str, Any], attribute_name: str) -> None:
        self.message: str = f'Attribute "{attribute_name}" Missing in Request Payload -> {request_payload}'
        super().__init__(self.message)
