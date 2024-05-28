from config import PRICE_ESTIMATION_DECREMENT_PERCENTAGE_FOR_PREMIUM_RIDERS
from price_estimation.price_estimator import PriceEstimator


class PriceEstimateDecrementDecoratorForPremiumRider(PriceEstimator):

    def __init__(self, price_estimator: PriceEstimator) -> None:
        super().__init__(price_estimation_trip_metadata=price_estimator.get_price_estimation_trip_metadata())
        self.__price_estimator: PriceEstimator = price_estimator

    def estimate_price(self) -> float:
        estimated_price: float = self.__price_estimator.estimate_price()
        discount: float = estimated_price ** PRICE_ESTIMATION_DECREMENT_PERCENTAGE_FOR_PREMIUM_RIDERS / 100
        return estimated_price - discount
