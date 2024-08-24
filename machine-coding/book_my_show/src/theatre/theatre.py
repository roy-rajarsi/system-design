from threading import Lock
from typing import List, Optional

from .auditorium import Auditorium


class Theatre:

    __theatre: Optional['Theatre'] = None
    __lock: Lock = Lock()
    __params_initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'Theatre':
        if cls.__theatre is None:
            cls.__lock.acquire(blocking=True, timeout=-1)
            if cls.__theatre is None:
                cls.__theatre = super().__new__(cls)
                cls.__theatre.__init__()
            cls.__lock.release()
        return cls.__theatre

    def __init__(self) -> None:
        if not self.__params_initialized:
            self.__auditoriums: List[Auditorium] = list()
            self.__auditorium_count: int = 0
            self.__params_initialized = True

    def get_auditoriums(self) -> List[Auditorium]:
        return [auditorium for auditorium in self.__auditoriums]

    def add_auditorium(self, auditorium_number: int) -> None:
        self.__class__.__lock.acquire(blocking=True, timeout=-1)
        self.__auditoriums.append(Auditorium(auditorium_number=auditorium_number))
        self.__class__.__lock.release()
