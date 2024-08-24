from datetime import datetime as DateTime
from typing import Final


class ShowMetaData:

    def __init__(self, show_name: str, show_start_time: DateTime, show_end_time: DateTime) -> None:
        self.__show_name: Final[str] = show_name
        self.__show_start_time: Final[DateTime] = show_start_time
        self.__show_end_time: Final[DateTime] = show_end_time

    def get_show_name(self) -> str:
        return self.__show_name

    def get_show_start_time(self) -> DateTime:
        return self.__show_start_time

    def get_show_end_time(self) -> DateTime:
        return self.__show_end_time
