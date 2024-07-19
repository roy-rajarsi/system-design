from threading import Lock
from typing import List, Optional


class Queue[T]:

    def __init__(self, max_size: int = 1000) -> None:
        self.__queue: List[T] = list()
        self.__queue_length: int = 0
        self.__max_size: int = max_size
        self.__lock: Lock = Lock()

    def enqueue(self, element: T) -> None:
        self.__lock.acquire(blocking=True, timeout=-1)
        if self.__queue_length == self.__max_size:
            raise Exception(f'Queue Overflow')

        self.__queue.append(element)
        self.__queue_length += 1
        self.__lock.release()

    def dequeue(self) -> Optional[T]:
        self.__lock.acquire(blocking=True, timeout=-1)
        element: Optional[T] = self.__queue.pop(0) if not self.is_empty() else None
        self.__lock.release()
        return element

    def is_empty(self) -> bool:
        self.__lock.acquire(blocking=True, timeout=-1)
        is_empty_status: bool = self.__queue_length == 0
        self.__lock.release()
        return is_empty_status

    def is_full(self) -> bool:
        self.__lock.acquire(blocking=True, timeout=-1)
        is_full_status: bool = self.__queue_length == self.__max_size
        self.__lock.release()
        return is_full_status
