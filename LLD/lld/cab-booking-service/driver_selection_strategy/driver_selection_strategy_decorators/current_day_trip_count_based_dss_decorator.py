from driver_attendance.driver_attendance import DriverAttendance
from driver_selection_strategy.driver_selection_strategy import DriverSelectionStrategy
from user.driver import Driver

from typing import List, Type
from collections import namedtuple


DriverToCurrentDayTripCount: Type['DriverToCurrentDayTripCount'] = namedtuple(typename='DriverToCurrentDayTripCount',
                                                                              field_names=['driver', 'current_day_trip_count'])


class CurrentDayTripCountBasedDriverSelectionStrategyDecorator(DriverSelectionStrategy):

    def __init__(self, driver_selection_strategy: DriverSelectionStrategy) -> None:
        super().__init__()
        self.__driver_selection_strategy: DriverSelectionStrategy = driver_selection_strategy

    def get_list_of_drivers(self) -> List[Driver]:
        list_of_drivers: List[Driver] = self.__driver_selection_strategy.get_list_of_drivers()
        list_of_driver_to_current_day_trip_count: List[DriverToCurrentDayTripCount] = [DriverToCurrentDayTripCount(driver=driver,
                                                                                                                   current_day_trip_count=DriverAttendance().attendance_dict.get(driver))
                                                                                       for driver in list_of_drivers]
        list_of_driver_to_current_day_trip_count.sort(key=lambda x: x[1])
        return [driver_to_current_day_trip_count.driver for driver_to_current_day_trip_count in list_of_driver_to_current_day_trip_count]
