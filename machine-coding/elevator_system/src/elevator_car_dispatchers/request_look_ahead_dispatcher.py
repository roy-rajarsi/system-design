from threading import Condition
import time
from typing import Dict, List, Optional, Tuple

from elevator.elevator_car import ElevatorCar
from enums.elevator_car_dispatch_direction import ElevatorCarDispatchDirection
from enums.elevator_car_states import ElevatorCarState
from .elevator_car_dispatcher import ElevatorCarDispatcher
from request import Request
from threads.elevator_car_gate_opening_thread import ElevatorCarGateOpeningThread


class RequestLookAheadDispatcher(ElevatorCarDispatcher):

    def __init__(self, elevator_car: ElevatorCar) -> None:
        super().__init__(elevator_car=elevator_car)
        self.__elevator_car_state: ElevatorCarState = ElevatorCarState.IDLE
        self.__current_dispatch_direction: ElevatorCarDispatchDirection = ElevatorCarDispatchDirection.NONE
        self.__request_count: int = 0
        self.__dispatch_requests: Dict[int, bool] = {floor: False for floor in self._elevator_car.get_floors_to_serve()}
        self.__served_requests: List[int] = list()
        self.__condition: Condition = Condition()
        self.__elevator_car_gate_opening_thread: ElevatorCarGateOpeningThread = ElevatorCarGateOpeningThread(name=f'ElevatorCarGateOpeningThread-{elevator_car.get_elevator_car_id()}',
                                                                                                             elevator_car=elevator_car)

    def get_served_requests(self) -> List[int]:
        served_requests: List[int]
        with self.__condition:
            served_requests = [floor for floor in self.__served_requests]
        return served_requests

    def schedule_request(self, request: Request) -> None:
        with self.__condition:
            if not self.__dispatch_requests.get(request.get_payload().get('floor')):
                self.__dispatch_requests[request.get_payload().get('floor')] = True
                self.__request_count += 1

    def get_next_requested_floor_and_dispatch_direction(self) -> Optional[Tuple[int, ElevatorCarDispatchDirection]]:
        if self.__current_dispatch_direction == ElevatorCarDispatchDirection.UP:
            floor: int
            for floor in range(self._elevator_car.get_current_floor(), self._elevator_car.get_max_floor_to_serve()):
                if self.__dispatch_requests.get(floor):
                    return floor, ElevatorCarDispatchDirection.UP
            for floor in range(self._elevator_car.get_current_floor() - 1, self._elevator_car.get_min_floor_to_serve(), -1):
                if self.__dispatch_requests.get(floor):
                    return floor, ElevatorCarDispatchDirection.DOWN
        elif self.__current_dispatch_direction == ElevatorCarDispatchDirection.DOWN:
            floor: int
            for floor in range(self._elevator_car.get_current_floor() - 1, self._elevator_car.get_min_floor_to_serve(), -1):
                if self.__dispatch_requests.get(floor):
                    return floor, ElevatorCarDispatchDirection.DOWN
            for floor in range(self._elevator_car.get_current_floor(), self._elevator_car.get_max_floor_to_serve()):
                if self.__dispatch_requests.get(floor):
                    return floor, ElevatorCarDispatchDirection.UP
        return None

    def serve(self) -> None:
        while True:
            with self.__condition:
                while self.__request_count == 0:
                    self.__elevator_car_state = ElevatorCarState.IDLE
                    self.__current_dispatch_direction = ElevatorCarDispatchDirection.NONE
                    self.__condition.wait(timeout=-1)

                next_requested_floor_and_dispatch_direction: Optional[Tuple[int, ElevatorCarDispatchDirection]] = self.get_next_requested_floor_and_dispatch_direction()

            next_requested_floor: int
            next_dispatch_direction: ElevatorCarDispatchDirection
            next_requested_floor, next_dispatch_direction = next_requested_floor_and_dispatch_direction
            self.__current_dispatch_direction = next_dispatch_direction

            self.dispatch(source_floor=self._elevator_car.get_current_floor(), destination_floor=next_requested_floor, elevator_dispatch_direction=next_dispatch_direction)

    def dispatch(self, source_floor: int, destination_floor: int, elevator_dispatch_direction: ElevatorCarDispatchDirection) -> None:
        assert self.__elevator_car_state == ElevatorCarState.IDLE and self._elevator_car.get_current_floor() == source_floor

        def serve_at_floor(floor_: int) -> None:
            self.__elevator_car_state = ElevatorCarState.IDLE
            self.__elevator_car_gate_opening_thread.open_elevator_car_gate()
            with self.__condition:
                self.__dispatch_requests[floor_] = False
                self.__served_requests.append(floor_)
                self.__request_count -= 1
            while not self.__elevator_car_gate_opening_thread.is_elevator_gate_closed():
                time.sleep(5)

        if source_floor == destination_floor:
            serve_at_floor(floor_=destination_floor)
            return None

        iterator: int = 1 if elevator_dispatch_direction == ElevatorCarDispatchDirection.UP else -1
        self.__elevator_car_state = ElevatorCarState.IN_MOTION
        for floor in range(source_floor, destination_floor, iterator):
            if floor != source_floor:
                self._elevator_car.set_current_floor(current_floor=floor)
                with self.__condition:
                    if self.__dispatch_requests.get(floor):
                        serve_at_floor(floor_=floor)
                        self.__elevator_car_state = ElevatorCarState.IN_MOTION
        serve_at_floor(floor_=destination_floor)
