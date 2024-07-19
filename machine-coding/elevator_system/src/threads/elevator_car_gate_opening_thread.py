from threading import Condition, Thread

from elevator.elevator_car import ElevatorCar


class ElevatorCarGateOpeningThread(Thread):

    def __init__(self, name: str, elevator_car: ElevatorCar) -> None:
        super().__init__(name=name)
        self.__elevator_car: ElevatorCar = elevator_car
        self.__should_open_gate: bool = False
        self.__condition: Condition = Condition()

    def open_elevator_car_gate(self) -> None:
        with self.__condition:
            self.__should_open_gate = True
            self.__condition.notify(n=1)

    def is_elevator_gate_closed(self) -> bool:
        return self.__should_open_gate

    def start(self) -> None:
        while True:
            with self.__condition:
                while not self.__should_open_gate:
                    self.__condition.wait(timeout=-1)
                self.__elevator_car.open_gate()
                self.__should_open_gate = False
