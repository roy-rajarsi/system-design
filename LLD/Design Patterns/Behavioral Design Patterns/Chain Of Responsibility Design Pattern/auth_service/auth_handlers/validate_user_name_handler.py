from auth_requests import UserNameValidationRequest
from auth_responses import UserNameValidationResponse
from .auth_handler import AuthHandler
from db import USER_DB


class UserNameValidationHandler(AuthHandler):

    """ Username Validation Handler Class for Authorization """

    def __init__(self) -> None:
        super().__init__()

    def process_auth_request(self, request: UserNameValidationRequest) -> UserNameValidationResponse:

        username: str = request.get_request_as_dict().get('username')
        user_id: int

        for user_id in USER_DB:
            if username == USER_DB.get(user_id).get('username'):
                return UserNameValidationResponse(response={
                    'user_id': user_id,
                    'password': request.get_request_as_dict().get('password')
                })

        raise Exception("User is not found")
