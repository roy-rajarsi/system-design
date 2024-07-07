from enums.parking_lot_entity_types import ParkingLotEntityType
from .parking_lot_entity import ParkingLotEntity


class EntryGate(ParkingLotEntity):

    def __init__(self, row_id: int, col_id, parking_lot_entity_type: ParkingLotEntityType, entry_gate_number: int) -> None:
        super().__init__(id=entry_gate_number, row_id=row_id, col_id=col_id, parking_lot_entity_type=parking_lot_entity_type)

