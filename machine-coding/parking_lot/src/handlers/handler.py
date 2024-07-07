from abc import ABC, abstractmethod
from typing import Optional

from request import Request
from response import Response


class Handler(ABC):

    def __init__(self) -> None:
        self.__next_handler: Optional['Handler'] = None

    def get_next_handler(self) -> Optional['Handler']:
        return self.__next_handler

    def set_next_handler(self, next_handler: Optional['Handler']) -> None:
        self.__next_handler = next_handler

    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass
