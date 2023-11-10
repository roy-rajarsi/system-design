from .response import Response

from random import randint


class AdminResponse(Response):

    """
    Handles response for admin
    Returns user_id, user_name, number_of_users_currently_logged_in, TPS in a server
    TPS -> Transactions per second
    """

    def __init__(self, user_id: int) -> None:
        self.__user_id: int = user_id
        self.__user_name = "demo_admin_user"
        self.__number_of_users_currently_logged_in: int = AdminResponse.__get_number_of_users_currently_logged_in()
        self.__tps: int = AdminResponse.__get_tps()

    @staticmethod
    def __get_number_of_users_currently_logged_in() -> int:

        # In Django may be some
        # Model instance get(number_of_users_currently_logged_in=number_of_users_currently_logged_in)

        return randint(100000, 999999)

    @staticmethod
    def __get_tps() -> int:
        return randint(1000, 5000) # Good TPS for starting a business

    def generate_response(self) -> dict:

        response: dict = dict()
        response["user_id"]: int = self.__user_id
        response["user_name"]: str = self.__user_name
        response["number_of_users_currently_logged_in"]: int = self.__number_of_users_currently_logged_in
        response["tps"]: int = self.__tps

        return response
