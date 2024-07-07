from typing import Final

from enums.vehicle_types import VehicleType


class Vehicle:

    def __init__(self, registration_number: str, vehicle_type: VehicleType) -> None:
        self.__registration_number: Final[str] = registration_number
        self.__vehicle_type: Final[VehicleType] = vehicle_type

    def get_registration_number(self) -> str:
        return self.__registration_number

    def get_vehicle_type(self) -> VehicleType:
        return self.__vehicle_type
