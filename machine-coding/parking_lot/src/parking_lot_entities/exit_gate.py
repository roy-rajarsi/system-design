from enums.parking_lot_entity_types import ParkingLotEntityType
from .parking_lot_entity import ParkingLotEntity


class ExitGate(ParkingLotEntity):

    def __init__(self, row_id: int, col_id, parking_lot_entity_type: ParkingLotEntityType, exit_gate_number: int) -> None:
        super().__init__(row_id=row_id, col_id=col_id, parking_lot_entity_type=parking_lot_entity_type)
        self.__exit_gate_number: int = exit_gate_number

    def get_exit_gate_number(self) -> int:
        return self.__exit_gate_number
