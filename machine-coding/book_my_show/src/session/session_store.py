from threading import Lock, Thread
from time import sleep
from typing import Dict, Optional
from uuid import UUID

from .session import Session


class SessionStore:

    def __init__(self) -> None:
        self.__active_sessions: Dict[UUID, Session] = dict()
        self.__expired_sessions: Dict[UUID, Session] = dict()
        self.__session_lock: Lock = Lock()
        self.__session_expiration_checking_thread: Thread = Thread(name=f'SessionExpirationCheckingThread', daemon=True, target=self.handle_session_expirations)
        self.__session_expiration_checking_thread.start()

    def add_session(self, session: Session) -> None:
        self.__session_lock.acquire(blocking=True, timeout=False)
        self.__active_sessions[session.get_session_id()] = session
        self.__session_lock.release()

    def get_session(self, session_id: UUID) -> Optional[Session]:
        return self.__active_sessions.get(session_id) if self.__active_sessions.get(session_id, None) is not None else self.__expired_sessions.get(session_id, None)

    def handle_session_expirations(self) -> None:
        while True:
            self.__session_lock.acquire(blocking=True, timeout=False)
            session_id: UUID
            session: Session
            for session_id, session in self.__active_sessions.items():
                if session.is_expired():
                    self.__expired_sessions[session_id] = self.__active_sessions.pop(session_id)
            self.__session_lock.release()
            sleep(5)
