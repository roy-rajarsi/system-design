from auth_requests import RateLimitRequest
from auth_responses import RateLimitResponse
from .auth_handler import AuthHandler
from db import USER_SESSION


class RateLimitHandler(AuthHandler):

    """ Authentication Class for Rate Limiting """

    def __init__(self) -> None:
        super().__init__()

    def process_auth_request(self, request: RateLimitRequest) -> RateLimitResponse:

        user_id: int = request.get_request_as_dict().get('user_id')

        return RateLimitResponse({
            'user_id': user_id,
            'password': request.get_request_as_dict().get('password'),
            'already_logged_in_status': user_id in USER_SESSION,
            'user_session_information': USER_SESSION
        })
