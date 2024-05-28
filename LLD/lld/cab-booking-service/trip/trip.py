from .trip_location import TripLocation
from .trip_metadata.trip_rider_metadata import RiderMetaData
from .trip_metadata.trip_driver_metadata import DriverMetaData

from enum import Enum


class TripStatus(Enum):

    TRIP_CONFIRMED = 'TRIP_CONFIRMED'
    TRIP_STARTED = 'TRIP_STARTED',
    TRIP_ONGOING = 'TRIP_ONGOING',
    TRIP_ENDED = 'TRIP_ENDED'


class Trip:

    def __init__(self, trip_location: TripLocation, estimated_price: float, rider_metadata: RiderMetaData, driver_metadata: DriverMetaData) -> None:
        self.__trip_location: TripLocation = trip_location
        self.__estimated_price: float = estimated_price
        self.__rider_metadata: RiderMetaData = rider_metadata
        self.__driver_metadata: DriverMetaData = driver_metadata
        self.__trip_state: TripStatus = TripStatus.TRIP_CONFIRMED

    def set_trip_state(self, trip_state) -> None:
        self.__trip_state = trip_state

