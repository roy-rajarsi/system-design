from typing import Any, Dict


class AttributeMissingInResponsePayloadException(Exception):

    def __init__(self, response_payload: Dict[str, Any], attribute_name: str) -> None:
        self.message: str = f'Attribute "{attribute_name}" Missing in Response Payload -> {response_payload}'
        super().__init__(self.message)
