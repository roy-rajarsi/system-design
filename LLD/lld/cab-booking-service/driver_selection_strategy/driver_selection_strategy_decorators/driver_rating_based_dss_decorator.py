from driver_selection_strategy.driver_selection_strategy import DriverSelectionStrategy
from user.driver import Driver

from typing import List, Type
from collections import namedtuple


DriverToDriverRating: Type['DriverToDriverRating'] = namedtuple(typename='DriverToDriverRating', field_names=['driver', 'driver_rating'])


class DriverRatingBasedDriverSelectionStrategy(DriverSelectionStrategy):

    def __init__(self, driver_selection_strategy: DriverSelectionStrategy) -> None:
        super().__init__()
        self.__driver_selection_strategy: DriverSelectionStrategy = driver_selection_strategy

    def get_list_of_drivers(self) -> List[Driver]:
        list_of_drivers: List[Driver] = self.__driver_selection_strategy.get_list_of_drivers()
        list_of_driver_to_driver_rating: List[DriverToDriverRating] = [DriverToDriverRating(driver=driver,
                                                                                            driver_rating=driver.get_rating())
                                                                       for driver in list_of_drivers]
        list_of_driver_to_driver_rating.sort(key=lambda x: x[1])
        return [driver_to_driver_rating.driver for driver_to_driver_rating in list_of_driver_to_driver_rating]
