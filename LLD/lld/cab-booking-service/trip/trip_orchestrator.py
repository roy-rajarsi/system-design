from user.rider import Rider
from user.driver import Driver
from location.location import Location
from .trip_location import TripLocation

from typing import List


class TripOrchestrator:

    def __init__(self, rider: Rider, trip_source: Location, trip_destination: Location) -> None:
        self.__rider: Rider = rider
        self.__trip_location: TripLocation = TripLocation(trip_source=trip_source, trip_destination=trip_destination)

    def manage_trip(self) -> None:
        pass

