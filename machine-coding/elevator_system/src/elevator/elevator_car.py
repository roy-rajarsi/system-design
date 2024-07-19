from copy import deepcopy
from time import sleep
from typing import Final, List


class ElevatorCar:

    def __init__(self, elevator_car_id: str, floors_to_serve: List[int]) -> None:
        self.__elevator_car_id: Final[str] = elevator_car_id
        self.__floors_to_serve: Final[List[int]] = floors_to_serve
        self.__min_floor_to_serve: Final[int] = floors_to_serve[0]
        self.__max_floor_to_serve: Final[int] = floors_to_serve[-1]
        self.__current_floor: int = self.__min_floor_to_serve

    def get_elevator_car_id(self) -> str:
        return self.__elevator_car_id

    def get_floors_to_serve(self) -> List[int]:
        return deepcopy(self.__floors_to_serve)

    def get_min_floor_to_serve(self) -> int:
        return self.__min_floor_to_serve

    def get_max_floor_to_serve(self) -> int:
        return self.__max_floor_to_serve

    def get_current_floor(self) -> int:
        return self.__current_floor

    def set_current_floor(self, current_floor: int) -> None:
        self.__current_floor = current_floor

    def open_gate(self) -> None:
        print(f'{self} :: Opened Gate....')
        sleep(5)
        print(f'{self} :: Closed Gate....')

    def __repr__(self) -> str:
        return f'ElevatorCar(Id: {self.get_elevator_car_id()} CurrentFloor: {self.get_current_floor()})'
