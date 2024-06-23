from collections.abc import Iterable, Iterator
from threading import Condition
from typing import List, Optional


class StreamIterator(Iterator):

    def __init__(self, stream: 'Stream') -> None:
        self.__stream: Stream = stream
        self.__index: int = 0

    def __next__(self) -> Optional[int]:
        with self.__stream.get_condition():
            while self.__stream.is_empty() or self.__index == len(self.__stream.get_queue()):
                self.__stream.get_condition().wait(timeout=-1)

            self.__index += 1
            print(f'Queue -> {self.__stream.get_queue()} IteratorIndex -> {self.__index-1}')
            return self.__stream.get_queue()[self.__index-1]


class Stream(Iterable):

    def __init__(self) -> None:
        self.__queue: List[int] = list()
        self.__condition: Condition = Condition()

    def push_to_stream(self, element: int) -> None:
        with self.__condition:
            self.__queue.append(element)
            self.__condition.notify(n=1)

    def get_queue(self) -> List[int]:
        return self.__queue

    def get_condition(self) -> Condition:
        return self.__condition

    def is_empty(self) -> bool:
        return len(self.__queue) == 0

    def __iter__(self) -> StreamIterator:
        return StreamIterator(stream=self)
