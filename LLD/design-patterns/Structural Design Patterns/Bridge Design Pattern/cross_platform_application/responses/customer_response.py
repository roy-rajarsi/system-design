from .response import Response

from random import randint
from typing import Optional


class CustomerResponse(Response):

    """
    Handles response for generic users -> Customers
    Returns user_id, user_name and friend_list of user
    """

    def __init__(self, user_id: int) -> None:

        self.__user_id: int = user_id
        self.__user_name: str = "demo_customer_user"
        self.__friend_list: list[Optional[int]] = self.__get_friend_list()

    def __get_friend_list(self) -> list[int]:

        """ Returns user id of friends for current user """

        # Fetch friend_list from some DB using the user_id and return the list
        # In Django may be some Model instance get(user_id = user_id).friend_list_ids

        user_id: int = self.__user_id
        friend_list: list[Optional[int]] = list()

        friend_user_id: int
        for _ in range(5):
            friend_user_id: int = randint(100, 999) # Lets say user_id ranges from 100 -> 999
            friend_list.append(friend_user_id)

        return friend_list

    def generate_response(self) -> dict:

        response: dict = dict()
        response["user_id"]: int = self.__user_id
        response["user_name"]: str = self.__user_name
        response["friend_list"]: list[Optional[int]] = self.__friend_list

        return response
