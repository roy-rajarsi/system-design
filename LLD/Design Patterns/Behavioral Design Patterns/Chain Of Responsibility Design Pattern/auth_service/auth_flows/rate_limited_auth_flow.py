from typing import Optional, Any

from .auth_flow import AuthFlow
from auth_handlers.auth_handler import AuthHandler
from auth_handlers.validate_user_name_handler import UserNameValidationHandler
from auth_handlers.rate_limit_handler import RateLimitHandler
from auth_handlers.validate_password_handler import PasswordValidationHandler
from auth_handlers.grant_permissions_handler import PermissionGrantHandler
from auth_requests import AuthRequest, UserNameValidationRequest, PasswordValidationRequest, PermissionGrantRequest, RateLimitRequest
from auth_responses import AuthResponse, RateLimitResponse


class RateLimitedAuthFlow(AuthFlow):

    def __init__(self) -> None:
        self.__head_handler: Optional[AuthHandler] = None
        self.__username_validation_handler: UserNameValidationHandler = UserNameValidationHandler()
        self.__rate_limit_handler: RateLimitHandler = RateLimitHandler()
        self.__password_validation_handler: PasswordValidationHandler = PasswordValidationHandler()
        self.__permission_grant_handler: PermissionGrantHandler = PermissionGrantHandler()

        self.generate_chain_of_responsibility()

    def generate_chain_of_responsibility(self) -> None:
        self.__head_handler = self.__username_validation_handler
        self.__username_validation_handler.set_next_handler(next_auth_handler=self.__rate_limit_handler)
        self.__rate_limit_handler.set_next_handler(next_auth_handler=self.__password_validation_handler)
        self.__password_validation_handler.set_next_handler(next_auth_handler=self.__permission_grant_handler)

    def process_auth_request(self, auth_request: dict[str, Any]) -> Optional[AuthResponse]:

        current_handler: AuthHandler = self.__head_handler
        request_artifacts: dict[str, Any] = auth_request
        response: Optional[AuthResponse] = None

        try:
            while current_handler is not None:
                auth_request: AuthRequest = RateLimitedAuthFlow.generate_auth_request_for_handler(
                    auth_handler=current_handler,
                    request_artifacts=request_artifacts)
                response = current_handler.process_auth_request(request=auth_request)

                if type(response) is RateLimitResponse and response.get_response_as_dict().get('already_logged_in_status'):
                    break

                request_artifacts = response.get_response_as_dict()
                current_handler = current_handler.get_next_auth_handler()

        except Exception as exception:
            print(f"Exception Occurred -> {exception}")
            response = None

        finally:
            return response

    @staticmethod
    def generate_auth_request_for_handler(auth_handler: AuthHandler, request_artifacts: dict[str, Any]) -> AuthRequest:

        if type(auth_handler) is UserNameValidationHandler:
            return UserNameValidationRequest({
                'username': request_artifacts.get('username'),
                'password': request_artifacts.get('password')
            })

        elif type(auth_handler) is RateLimitHandler:
            return RateLimitRequest({
                'user_id': request_artifacts.get('user_id'),
                'password': request_artifacts.get('password')
            })

        elif type(auth_handler) is PasswordValidationHandler:
            return PasswordValidationRequest({
                'user_id': request_artifacts.get('user_id'),
                'password': request_artifacts.get('password')
            })

        elif type(auth_handler) is PermissionGrantHandler:
            return PermissionGrantRequest({
                'user_id': request_artifacts.get('user_id'),
                'password_matched': request_artifacts.get('password_matched')
            })

        else:
            raise Exception(f"Invalid Auth Handler -> {auth_handler}")
