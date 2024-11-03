from typing import Final, List


class MultiLevelCacheMonitor:

    def __init__(self, read_queue_length: int, write_queue_length: int) -> None:
        self.__read_queue_length: Final[int] = read_queue_length
        self.__write_queue_length: Final[int] = write_queue_length
        self.__read_queue: List[float] = list()
        self.__write_queue: List[float] = list()

    def add_read_time(self, read_time: float) -> None:
        if len(self.__read_queue) == self.__read_queue_length:
            self.__read_queue.pop(0)
        self.__read_queue.append(read_time)

    def add_write_time(self, write_time: float) -> None:
        if len(self.__write_queue) == self.__write_queue_length:
            self.__write_queue.pop(0)
        self.__write_queue.append(write_time)

    def get_mean_of_read_times(self) -> float:
        return sum(self.__read_queue) / len(self.__read_queue)

    def get_mean_of_write_times(self) -> float:
        return sum(self.__write_queue) / len(self.__write_queue)
