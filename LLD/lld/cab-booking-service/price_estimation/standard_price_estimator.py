from config import PRICE_RATE_PER_KM
from location.location import Location
from .price_estimator import PriceEstimator
from .price_estimation_metadata.price_estimation_trip_metadata import PriceEstimationTripMetaData
from trip.trip_location import TripLocation


class StandardPriceEstimator(PriceEstimator):

    def __init__(self, price_estimation_trip_metadata: PriceEstimationTripMetaData) -> None:
        super().__init__(price_estimation_trip_metadata=price_estimation_trip_metadata)

    def estimate_price(self) -> float:
        trip_location: TripLocation = self.get_price_estimation_trip_metadata().get_trip_location()
        euclidean_distance: float = StandardPriceEstimator.__calculate_euclidean_distance(source=trip_location.get_trip_source(),
                                                                                          destination=trip_location.get_trip_destination())
        return PRICE_RATE_PER_KM.get(trip_location.get_trip_city()) * euclidean_distance

    @staticmethod
    def __calculate_euclidean_distance(source: Location, destination: Location) -> float:
        return ((source.latitude - destination.latitude) ** 2 + (source.longitude - destination.longitude) ** 2) ** 0.5
