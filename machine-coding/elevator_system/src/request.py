from copy import deepcopy
from typing import Any, Dict, Final
from uuid import uuid4 as UUID4

from elevator.elevator_car import ElevatorCar
from enums.request_type import RequestType


class Request:

    def __init__(self, floor: int, elevator_car: ElevatorCar, request_type: RequestType) -> None:
        self.__request_id: UUID4 = UUID4()
        self.__payload: Final[Dict[str, Any]] = {
            'floor': floor,
            'elevator_car': elevator_car    # TODO: In actual implementation this should be the Button Panel
        }
        self.__request_type: RequestType = request_type

    def get_request_type(self) -> RequestType:
        return self.__request_type

    def get_payload(self) -> Dict[str, Any]:
        return deepcopy(self.__payload)

    def __repr__(self) -> str:
        return f'Request(Id: {self.__request_id} Payload: {self.__payload})'
