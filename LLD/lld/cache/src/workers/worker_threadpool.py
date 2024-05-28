from data_structures.queue import Queue
from worker_thread import WorkerThread

from typing import Callable, Dict


class WorkerThreadPool:

    def __init__(self, name: str, worker_count: int, target_function: Callable) -> None:
        self.__name: str = name
        self.__worker_count: int = worker_count
        self.__target_function: Callable = target_function
        self.__threadpool: Dict[int, WorkerThread] = WorkerThreadPool.__initiate_threadpool(threadpool_name=self.__name, worker_count=self.__worker_count, target_function=target_function)
        self.start_threads()

    def get_worker_thread_for_a_hash_value(self, hash_value: int) -> WorkerThread:
        return self.__threadpool.get(hash_value % self.__worker_count)

    def start_threads(self) -> None:
        worker_thread: WorkerThread
        for worker_thread in self.__threadpool.values():
            worker_thread.start()

    @staticmethod
    def __initiate_threadpool(threadpool_name: str, worker_count: int, target_function: Callable) -> Dict[int, WorkerThread]:
        threadpool: Dict[int, WorkerThread] = dict()

        index_: int
        for index_ in range(worker_count):
            thread_name: str = f'{threadpool_name}_Thread_{index_+1}'
            worker_thread: WorkerThread = WorkerThread(name=thread_name, task_queue=Queue(), target_function=target_function)
            threadpool[index_] = worker_thread

        return threadpool
