from trip_state import TripState
from trip.trip_location import TripLocation
from trip.trip_metadata.trip_rider_metadata import RiderMetaData
from trip.trip import Trip


class TripStateIdle(TripState):

    def __init__(self) -> None:
        super().__init__()

    def request_trip(self, trip_location: TripLocation, rider_metadate: RiderMetaData) -> None:
        from trip_state_driver_matching import TripStateDriverMatching

        if self.get_trip() is None:
            raise Exception('Trip is not set. Please set trip for the current TripState')

        self.get_trip().set_trip_state(trip_state=TripStateDriverMatching())



