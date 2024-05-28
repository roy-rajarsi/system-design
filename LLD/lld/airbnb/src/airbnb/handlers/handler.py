from requests.request import Request
from responses.response import Response

from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):

    def __init__(self) -> None:
        self.next_handler: Optional[Handler] = None

    def get_next_handler(self) -> Optional['Handler']:
        return self.next_handler

    def set_next_handler(self, next_handler: Optional['Handler']) -> None:
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass
