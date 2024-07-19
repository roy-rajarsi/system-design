from abc import ABC, abstractmethod

from elevator.elevator_car import ElevatorCar
from request import Request


class ElevatorCarDispatcher(ABC):

    def __init__(self, elevator_car: ElevatorCar) -> None:
        self._elevator_car: ElevatorCar = elevator_car

    @abstractmethod
    def schedule_request(self, request: Request) -> None:
        pass

    @abstractmethod
    def serve(self) -> None:
        pass
