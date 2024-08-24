from threading import Lock
from typing import Final, List
from uuid import uuid4, UUID


class User:

    __users: List['User'] = list()
    __lock: Lock = Lock()

    def __init__(self, username: str) -> None:
        self.__class__.__lock.acquire(blocking=True, timeout=-1)
        self.__user_id: Final[UUID] = uuid4()
        self.__username: str = username
        self.__class__.__users.append(self)
        self.__class__.__lock.release()

    def get_user_id(self) -> UUID:
        return self.__user_id

    def get_username(self) -> str:
        return self.__username

    def __repr__(self) -> str:
        return f'{self.__username}'
