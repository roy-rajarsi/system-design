from threading import Condition, Thread

from data_structures.queue import Queue
from elevator_car_dispatchers.elevator_car_dispatcher import ElevatorCarDispatcher
from request import Request


class RequestSchedulingThread(Thread):

    def __init__(self, name: str, request_queue: Queue[Request], condition: Condition, elevator_car_dispatcher: ElevatorCarDispatcher) -> None:
        super().__init__(name=name)
        self.__request_queue: Queue[Request] = request_queue
        self.__condition: Condition = condition
        self.__elevator_car_dispatcher: ElevatorCarDispatcher = elevator_car_dispatcher

    def get_request_queue(self) -> Queue[Request]:
        return self.__request_queue

    def get_condition(self) -> Condition:
        return self.__condition

    def schedule_request(self, request: Request) -> None:
        with self.__condition:
            self.__request_queue.enqueue(element=request)

    def run(self) -> None:
        while True:
            with self.__condition:
                while self.__request_queue.is_empty():
                    self.__condition.wait(timeout=-1)

                request: Request = self.__request_queue.dequeue()
                self.__elevator_car_dispatcher.schedule_request(request=request)
