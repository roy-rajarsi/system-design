from typing import Union
from enum import Enum
from datetime import datetime


class UserType(Enum):

    ADMIN = 'ADMIN',
    NORMAL_USER = 'NORMAL_USER'


USER_DB: dict[int, dict[str, Union[str, int, bool]]] = {
    1243: {
        'username': 'demo_user1',
        'user_id': 1243,
        'password': 'demo_user1_password',
        'is_admin': False,
    },
    5623: {
        'username': 'admin_user1',
        'user_id': 5623,
        'password': 'admin_user1_password',
        'is_admin': True,
    }
}

USER_PERMISSIONS: dict[UserType, list[str]] = {

    UserType.ADMIN: [
        'ADMIN_PERMISSION_1',
        'ADMIN_PERMISSION_2',
        'NORMAL_USER_PERMISSION_1',
        'NORMAL_USER_PERMISSION_2',
        'NORMAL_USER_PERMISSION_3'
    ],

    UserType.NORMAL_USER: [
        'NORMAL_USER_PERMISSION_1',
        'NORMAL_USER_PERMISSION_2',
        'NORMAL_USER_PERMISSION_3',
    ]
}


class UserSessionInformation:

    def __init__(self, user_id: int, last_logged_in: datetime, permissions: list[str]) -> None:
        self.__user_id: int = user_id
        self.__last_logged_in: datetime = last_logged_in
        self.__permissions: list[str] = permissions

    def get_session_information_as_dict(self) -> dict[str, Union[int, datetime, list[str]]]:
        return {
            'user_id': self.__user_id,
            'last_logged_in': self.__last_logged_in,
            'permissions': self.__permissions
        }

    def __repr__(self) -> str:
        return f"User Session Information -> {self.get_session_information_as_dict()}"

    def set_last_logged_in_time(self, last_logged_in_time: datetime) -> None:
        self.__last_logged_in = last_logged_in_time


USER_SESSION: dict[int, UserSessionInformation] = dict()
