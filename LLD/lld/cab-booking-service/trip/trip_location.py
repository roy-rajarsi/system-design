from location.location import Location

from enum import Enum


class TripCity(Enum):

    TOWN = 'TOWN',
    CITY = 'CITY',
    METRO_CITY = 'METRO_CITY'


class TripLocation:

    def __init__(self, trip_source: Location, trip_destination: Location) -> None:
        self.__trip_source: Location = trip_source
        self.__trip_destination: Location = trip_destination
        self.__trip_city: TripCity = self.get_trip_city()

    def get_trip_source(self) -> Location:
        return self.__trip_source

    def get_trip_destination(self) -> Location:
        return self.__trip_destination

    def get_trip_city(self) -> TripCity:

        # Based on the Trip Source and Trip Distance returns in what kind of city the trip is going to happen
        if self.__trip_source:
            return TripCity.METRO_CITY

    def __repr__(self) -> str:
        return f'TripSource: {self.__trip_source} -> TripDestination: {self.__trip_destination} TripCity: {self.__trip_city}'
