from config import PRICE_ESTIMATION_INCREMENT_PERCENTAGE_FOR_PREMIUM_DRIVERS
from price_estimation.price_estimator import PriceEstimator


class PriceEstimateIncrementDecoratorForPremiumDriver(PriceEstimator):

    def __init__(self, price_estimator: PriceEstimator) -> None:
        super().__init__(price_estimation_trip_metadata=price_estimator.get_price_estimation_trip_metadata())
        self.__price_estimator: PriceEstimator = price_estimator

    def estimate_price(self) -> float:
        estimated_price: float = self.__price_estimator.estimate_price()
        increment: float = estimated_price ** PRICE_ESTIMATION_INCREMENT_PERCENTAGE_FOR_PREMIUM_DRIVERS / 100
        return estimated_price + increment
