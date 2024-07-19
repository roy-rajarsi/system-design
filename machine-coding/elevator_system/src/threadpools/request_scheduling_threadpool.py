from threading import Condition
from typing import Dict, List

from data_structures.queue import Queue
from elevator_car_dispatchers.elevator_car_dispatcher import ElevatorCarDispatcher
from request import Request
from threads.request_scheduling_thread import RequestSchedulingThread


class RequestSchedulingThreadpool:

    def __init__(self, elevator_car_dispatchers: List[ElevatorCarDispatcher]) -> None:
        self.__elevator_car_dispatchers: List[ElevatorCarDispatcher] = elevator_car_dispatchers
        self.__thread_count: int = len(elevator_car_dispatchers)
        self.__threadpool: List[RequestSchedulingThread] = [RequestSchedulingThread(name=f'RequestSchedulingThread-{thread_index}',
                                                                                    request_queue=Queue(),
                                                                                    condition=Condition(),
                                                                                    elevator_car_dispatcher=elevator_car_dispatcher) for thread_index, elevator_car_dispatcher in enumerate(self.__elevator_car_dispatchers)]
        self.__elevator_car_dispatcher_to_request_scheduling_thread_dict: Dict[ElevatorCarDispatcher, RequestSchedulingThread] = {elevator_car_dispatcher: request_scheduling_thread
                                                                                                                                  for elevator_car_dispatcher, request_scheduling_thread in zip(self.__elevator_car_dispatchers, self.__threadpool)}

    def start(self) -> None:
        request_scheduling_thread: RequestSchedulingThread
        for request_scheduling_thread in self.__threadpool:
            request_scheduling_thread.start()

    def schedule_request(self, elevator_car_dispatcher: ElevatorCarDispatcher, request: Request) -> None:
        self.__elevator_car_dispatcher_to_request_scheduling_thread_dict.get(elevator_car_dispatcher).schedule_request(request=request)
