from typing import Any, Dict


class ValidationError(Exception):

    def __init__(self, attribute: str, payload: Dict[str, Any]) -> None:
        super().__init__(f'{attribute} is missing in {payload}')
