from enums.parking_lot_entity_types import ParkingLotEntityType
from enums.parking_status import ParkingStatus
from enums.parking_spot_types import ParkingSpotType
from .parking_lot_entity import ParkingLotEntity


class ParkingSpot(ParkingLotEntity):

    def __init__(self, row_id: int, col_id, parking_lot_entity_type: ParkingLotEntityType, parking_spot_number: int, parking_spot_type: ParkingSpotType) -> None:
        super().__init__(id=parking_spot_number, row_id=row_id, col_id=col_id, parking_lot_entity_type=parking_lot_entity_type)
        self.__parking_status: ParkingStatus = ParkingStatus.NOT_PARKED
        self.__parking_spot_type: ParkingSpotType = parking_spot_type

    def get_parking_status(self) -> ParkingStatus:
        return self.__parking_status

    def get_parking_spot_type(self) -> ParkingSpotType:
        return self.__parking_spot_type

    def set_parking_status(self, parking_status: ParkingStatus) -> None:
        self.__parking_status = parking_status
