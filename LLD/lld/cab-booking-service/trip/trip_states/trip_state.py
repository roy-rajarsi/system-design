from trip.trip import Trip
from trip.trip_location import TripLocation
from trip.trip_metadata.trip_rider_metadata import RiderMetaData
from trip.trip_metadata.trip_driver_metadata import DriverMetaData

from abc import ABC
from typing import Optional


class TripState(ABC):

    def __init__(self) -> None:
        self._trip: Optional[Trip] = None

    def get_trip(self) -> Optional[Trip]:
        return self._trip

    def set_trip(self, trip: Trip) -> None:
        if self._trip is not None:
            raise Exception('Trip is already set. Please create a new TripState() for setting a new trip')
        self._trip = trip

    def request_trip(self, trip_location: TripLocation, rider_metadate: RiderMetaData) -> None:
        raise Exception(f'Cannot request trip from {self}')

    def match_driver(self) -> None:
        raise Exception(f'Cannot match driver from {self}')


