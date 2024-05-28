from user.driver import Driver

from typing import DefaultDict, Optional
from collections import defaultdict


class DriverAttendance:

    __driver_attendance_instance: Optional['DriverAttendance'] = None

    def __new__(cls, *args, **kwargs) -> 'DriverAttendance':

        if cls.__driver_attendance_instance is None:
            cls.__driver_attendance_instance = super(DriverAttendance, cls).__new__(cls)
            cls.__driver_attendance_instance.attendance_dict: DefaultDict[Driver, int] = defaultdict()

        return cls.__driver_attendance_instance

    def initialize_driver_attendance(self) -> None:
        self.__driver_attendance_instance.attendance_dict = dict()
