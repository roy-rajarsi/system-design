from abc import ABC, abstractmethod
from typing import Optional

from auth_requests import AuthRequest
from auth_responses import AuthResponse


class AuthHandler(ABC):

    """ Base Authentication and Authorization Handler Class """

    def __init__(self) -> None:
        self._next_handler: Optional[AuthHandler] = None

    def get_next_auth_handler(self) -> Optional['AuthHandler']:
        return self._next_handler

    def set_next_handler(self, next_auth_handler: 'AuthHandler') -> None:
        self._next_handler = next_auth_handler

    @abstractmethod
    def process_auth_request(self, request: AuthRequest) -> AuthResponse:
        pass
