from datetime import datetime

from auth_requests import PermissionGrantRequest
from auth_responses import PermissionGrantResponse
from db import UserType, USER_DB, USER_PERMISSIONS, USER_SESSION, UserSessionInformation
from .auth_handler import AuthHandler


class PermissionGrantHandler(AuthHandler):

    """ Permission Granting Handler Class for Authorization """

    def __init__(self) -> None:
        super().__init__()

    def process_auth_request(self, request: PermissionGrantRequest) -> PermissionGrantResponse:

        user_id: int = request.get_request_as_dict().get('user_id')
        password_matched: bool = request.get_request_as_dict().get('password_matched')

        permission_list: list[str] = list()

        if password_matched:
            user_type: UserType = UserType.ADMIN if USER_DB.get(user_id).get('is_admin') else UserType.NORMAL_USER
            permission_list = USER_PERMISSIONS.get(user_type).copy()

            USER_SESSION[user_id] = UserSessionInformation(user_id=user_id,
                                                           last_logged_in=datetime.now(),
                                                           permissions=permission_list)

        return PermissionGrantResponse({
            'user_id': user_id,
            'permission_granted': password_matched,
            'permissions': permission_list
        })
