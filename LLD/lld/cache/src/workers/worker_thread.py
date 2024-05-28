from data_structures.queue import Queue
from request import Request

from threading import Thread
from time import sleep
from typing import Callable


class WorkerThread(Thread):

    def __init__(self, name: str, task_queue: Queue, target_function: Callable) -> None:
        super().__init__(name=name, target=target_function, kwargs={'TaskQueue': task_queue})
        self.__target_function: Callable = target_function
        self.__task_queue: Queue = task_queue

    def get_target_function(self) -> Callable:
        return self.__target_function

    def get_task_queue(self) -> Queue:
        return self.__task_queue

    def run(self) -> None:
        while True:
            if not self.__task_queue.is_empty():
                request: Request = self.__task_queue.dequeue()
            else:
                sleep(5)

    def __repr__(self) -> str:
        return f'WorkerThread(Ident: {self.ident} Name: {self.name} Target: {self.get_target_function()} TaskQueue: {self.__task_queue})'
