from threading import Lock
from typing import Dict, List, Optional, Tuple, final

from decorators.thread_safe import thread_safe
from enums.parking_lot_entity_types import ParkingLotEntityType
from parking_lot_entities.parking_lot_entity import ParkingLotEntity
from parking_lot_entities.entry_gate import EntryGate
from parking_lot_entities.exit_gate import ExitGate
from parking_lot_entities.parking_spot import ParkingSpot


@final
class ParkingLot:

    __parking_lot: Optional['ParkingLot'] = None
    __lock: Lock = Lock()
    __params_initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'ParkingLot':
        if cls.__parking_lot is None:
            cls.__lock.acquire(blocking=True, timeout=-1)
            if cls.__parking_lot is None:
                cls.__parking_lot = super().__new__(cls=cls)
                cls.__parking_lot.__init__()
            cls.__lock.release()
        return cls.__parking_lot

    def __init__(self) -> None:
        if not self.__class__.__params_initialized:
            self.__entry_gates: List[EntryGate] = list()
            self.__exit_gates: List[ExitGate] = list()
            self.__parking_spots: List[ParkingSpot] = list()
            self.__entry_gates_count: int = 0
            self.__exit_gates_count: int = 0
            self.__parking_spots_count: int = 0
            self.__distance_dict: Dict[Tuple[ParkingLotEntity, ParkingLotEntity], float] = dict()
            self.__class__.__params_initialized = True

    @thread_safe(lock=__lock)
    def add_entry_gate(self, row_id: int, col_id: int) -> EntryGate:
        self.__entry_gates_count += 1
        entry_gate: EntryGate = EntryGate(entry_gate_number=self.__entry_gates_count, row_id=row_id, col_id=col_id, parking_lot_entity_type=ParkingLotEntityType.ENTRY_GATE)
        self.__entry_gates.append(entry_gate)
        return entry_gate

    @thread_safe(lock=__lock)
    def add_exit_gate(self, row_id: int, col_id: int) -> ExitGate:
        self.__exit_gates_count += 1
        exit_gate: ExitGate = ExitGate(exit_gate_number=self.__exit_gates_count, row_id=row_id, col_id=col_id, parking_lot_entity_type=ParkingLotEntityType.EXIT_GATE)
        self.__exit_gates.append(exit_gate)
        return exit_gate

    @thread_safe(lock=__lock)
    def add_parking_spot(self, row_id: int, col_id: int) -> ParkingSpot:
        self.__parking_spots_count += 1
        parking_spot: ParkingSpot = ParkingSpot(parking_spot_number=self.__parking_spots_count, row_id=row_id, col_id=col_id, parking_lot_entity_type=ParkingLotEntityType.PARKING_SPOT)
        self.__parking_spots.append(parking_spot)
        return parking_spot

    @thread_safe
    def get_entry_gates(self) -> List[EntryGate]:
        return self.__entry_gates
