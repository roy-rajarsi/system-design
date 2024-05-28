from trip_state import TripState
from trip.trip import Trip

from time import sleep


class TripStateDriverMatching(TripState):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def start_driver_matching(trip: Trip) -> None:
        print(f'Searching for Drivers...')
        sleep(secs=5)



    def confirm_trip(self, trip: Trip) -> None:
        if self.get_trip() is None:
            raise Exception('Trip is not set. Please set trip for the current TripState')

        trip.set_trip_state(trip_state=TripStateTripConfirmed())

    def cancel_trip_from_rider(self, trip: Trip) -> None:
        from trip_state_idle import TripStateIdle

        if self.get_trip() is None:
            raise Exception('Trip is not set. Please set trip for the current TripState')

        trip.set_trip_state(trip_state=TripStateIdle())
