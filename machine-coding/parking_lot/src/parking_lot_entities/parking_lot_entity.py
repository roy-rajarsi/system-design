from abc import ABC
from uuid import UUID, uuid4
from typing import Final

from enums.parking_lot_entity_types import ParkingLotEntityType


class ParkingLotEntity(ABC):

    def __init__(self, row_id: int, col_id, parking_lot_entity_type: ParkingLotEntityType) -> None:
        self.__id: Final[UUID] = uuid4()
        self.__row_id: Final[int] = row_id
        self.__col_id: Final[int] = col_id
        self.__parking_lot_entity_type: Final[ParkingLotEntityType] = parking_lot_entity_type

    def get_id(self) -> UUID:
        return self.__id

    def get_row_id(self) -> int:
        return self.__row_id

    def get_col_id(self) -> int:
        return self.__col_id

    def get_parking_lot_entity_type(self) -> ParkingLotEntityType:
        return self.__parking_lot_entity_type
