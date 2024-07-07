from typing import Any, Dict, Optional

from .response import Response


class NoneResponse(Response):

    def __init__(self, payload: Optional[Dict[Any, str]] = None) -> None:
        super().__init__(payload=payload)
