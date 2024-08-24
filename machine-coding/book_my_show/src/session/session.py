from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
from typing import Any, Dict, Final, Optional
from uuid import uuid4, UUID

from users.user import User


SESSION_TIMEOUT: int = 10


class Session:

    def __init__(self, user: User, session_payload: Optional[Dict[str, Any]] = None, session_timeout: int = SESSION_TIMEOUT) -> None:
        self.__session_id: Final[UUID] = uuid4()
        self.__user: Final[User] = user
        self.__session_payload: Dict[str, Any] = session_payload if session_payload is not None else dict()
        self.__session_creation_timestamp: Final[DateTime] = DateTime.now()
        self.__session_timeout: Final[TimeDelta] = TimeDelta(seconds=session_timeout)
        self.__session_expiry_timestamp: Final[DateTime] = self.__session_creation_timestamp + self.__session_timeout
        self.__expired: bool = self.is_expired()

    def get_session_id(self) -> UUID:
        return self.__session_id

    def get_user(self) -> User:
        return self.__user

    def get_session_payload(self) -> Dict[str, Any]:
        return self.__session_payload

    def set_session_payload(self, session_payload: Dict[str, Any]):
        self.__session_payload = session_payload

    def get_session_creation_timestamp(self) -> DateTime:
        return self.__session_creation_timestamp

    def get_session_timeout(self) -> TimeDelta:
        return self.__session_timeout

    def get_session_expiry_timestamp(self) -> DateTime:
        return self.__session_expiry_timestamp

    def is_expired(self) -> bool:
        return DateTime.now() >= self.__session_expiry_timestamp

    def expire_session(self) -> None:
        self.__expired = True

    def __repr__(self) -> str:
        return f'Session(Id: {self.__session_id} User: {self.__user} Expired: {self.is_expired()} Payload: {self.__session_payload})'
