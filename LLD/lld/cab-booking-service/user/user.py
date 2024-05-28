from trip.trip import Trip

from abc import ABC
from enum import Enum
from typing import List


class UserType(Enum):

    USER_RIDER = 'USER_RIDER'
    USER_DRIVER = 'USER_DRIVER'


class User(ABC):

    def __init__(self, user_id: int, username: str, user_type: UserType) -> None:
        self.__user_id: int = user_id
        self.__username: str = username
        self.__user_type: UserType = user_type
        self.__rating: float = 0
        self.__trip_history: List[Trip] = list()

    def get_user_id(self) -> int:
        return self.__user_id

    def get_username(self) -> str:
        return self.__username

    def get_user_type(self) -> UserType:
        return self.__user_type

    def get_rating(self) -> float:
        return self.__rating

    def set_rating(self, rating: float) -> None:
        self.__rating = rating

    def get_trip_history(self) -> List[Trip]:
        return self.__trip_history

    def add_trip_to_trip_history(self, trip: Trip) -> None:
        self.__trip_history.append(trip)

    def __repr__(self) -> str:
        return f'{self.__user_type}(UserId: {self.__user_id} Username: {self.__username} Rating: {self.__rating})'
