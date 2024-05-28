from trip.trip_location import TripLocation
from trip.trip_metadata.trip_rider_metadata import RiderMetaData
from trip.trip_metadata.trip_driver_metadata import DriverMetaData


class PriceEstimationTripMetaData:

    def __init__(self, trip_location: TripLocation, rider_metadata: RiderMetaData, driver_metadata: DriverMetaData) -> None:
        self.__trip_location: TripLocation = trip_location
        self.__rider_metadata: RiderMetaData = rider_metadata
        self.__driver_metadata: DriverMetaData = driver_metadata

    def get_trip_location(self) -> TripLocation:
        return self.__trip_location

    def get_rider_metadata(self) -> RiderMetaData:
        return self.__rider_metadata

    def get_driver_metadata(self) -> DriverMetaData:
        return self.__driver_metadata

    def __repr__(self) -> str:
        return f'PriceEstimationTripMetaData(TripLocation: {self.__trip_location} Rider: {self.__rider_metadata} Driver: {self.__driver_metadata})'
