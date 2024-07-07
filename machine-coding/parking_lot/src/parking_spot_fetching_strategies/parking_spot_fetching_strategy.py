from abc import ABC, abstractmethod
from typing import Optional

from parking_lot_entities.entry_gate import EntryGate
from parking_lot_entities.parking_spot import ParkingSpot


class ParkingSpotFetchingStrategy(ABC):

    @staticmethod
    @abstractmethod
    def fetch_parking_spot(entry_gate: EntryGate) -> Optional[ParkingSpot]:
        pass
