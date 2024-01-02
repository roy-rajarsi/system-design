from abc import ABC, abstractmethod

from auth_handlers.auth_handler import AuthHandler
from auth_requests import AuthRequest
from auth_responses import AuthResponse


class AuthFlow(ABC):

    @abstractmethod
    def generate_chain_of_responsibility(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def generate_auth_request_for_handler(auth_handler: AuthHandler, auth_response_from_previous_handler: AuthResponse) -> AuthRequest:
        pass

    @abstractmethod
    def process_auth_request(self, auth_request: AuthRequest) -> AuthResponse:
        pass
