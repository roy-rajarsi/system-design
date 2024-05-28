from abc import ABC, abstractmethod
from .price_estimation_metadata.price_estimation_trip_metadata import PriceEstimationTripMetaData


class PriceEstimator(ABC):

    def __init__(self, price_estimation_trip_metadata: PriceEstimationTripMetaData) -> None:
        self.__price_estimation_trip_metadata: PriceEstimationTripMetaData = price_estimation_trip_metadata

    def get_price_estimation_trip_metadata(self) -> PriceEstimationTripMetaData:
        return self.__price_estimation_trip_metadata

    @abstractmethod
    def estimate_price(self) -> float:
        pass
