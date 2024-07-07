from typing import Any, Dict, Optional

from .request import Request


class NoneRequest(Request):

    def __init__(self, payload: Optional[Dict[Any, str]] = None) -> None:
        super().__init__(payload=payload)
