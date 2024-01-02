from auth_requests import PasswordValidationRequest
from auth_responses import PasswordValidationResponse
from .auth_handler import AuthHandler
from db import USER_DB


class PasswordValidationHandler(AuthHandler):

    """ Password Validation Handler Class for Authorization """

    def __init__(self) -> None:
        super().__init__()

    def process_auth_request(self, request: PasswordValidationRequest) -> PasswordValidationResponse:

        user_id: int = request.get_request_as_dict().get('user_id')
        password: str = request.get_request_as_dict().get('password')

        password_matched: bool = (USER_DB.get(user_id).get('password') == password)

        return PasswordValidationResponse({
                'user_id': user_id,
                'password_matched': password_matched
            })
