from threading import Lock
from datetime import datetime as Datetime
from typing import Dict, Final, Optional
from uuid import uuid4, UUID

from decorators.thread_safe import thread_safe
from parking_lot_entities.parking_spot import ParkingSpot
from vehicles.vehicle import Vehicle


class Parking:

    __parkings: Dict[UUID, 'Parking'] = dict()
    __lock: Lock = Lock()

    def __init__(self, parking_spot: ParkingSpot, vehicle: Vehicle) -> None:
        self.__ticket_id: Final[UUID] = uuid4()
        self.__parking_spot: Final[ParkingSpot] = parking_spot
        self.__vehicle: Final[Vehicle] = vehicle
        self.__parked_at: Final[Datetime] = Datetime.now()
        self.__exit_time: Optional[Datetime] = None
        self.__is_active_parking: bool = True
        self.__class__.add_parking_to_parkings(parking=self)

    def get_ticket_id(self) -> UUID:
        return self.__ticket_id

    @classmethod
    @thread_safe(lock=__lock)
    def get_parking(cls, ticket_id: UUID) -> Optional['Parking']:
        return cls.__parkings.get(ticket_id, None)

    def get_parked_at_time(self) -> Datetime:
        return self.__parked_at

    def set_exit_time(self) -> None:
        self.__exit_time = Datetime.now()

    def set_parking_to_inactive(self) -> None:
        self.__is_active_parking = False

    @classmethod
    @thread_safe(lock=__lock)
    def add_parking_to_parkings(cls, parking: 'Parking') -> None:
        cls.__parkings[parking.get_ticket_id()] = parking
