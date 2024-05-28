from .user import User, UserType


class Driver(User):

    def __init__(self, user_id: int, username: str, cab_number: str, cab_color: str) -> None:
        super().__init__(user_id=user_id, username=username, user_type=UserType.USER_DRIVER)

        self.__cab_number: str = cab_number
        self.__cab_color: str = cab_color

    def get_cab_number(self) -> str:
        return self.__cab_number

    def set_cab_number(self, cab_number: str) -> None:
        self.__cab_number = cab_number

    def get_cab_color(self) -> str:
        return self.__cab_color

    def set_cab_color(self, cab_color: str) -> None:
        self.__cab_color = cab_color

    def __repr__(self) -> str:
        return f'{super().__repr__()} CabNumber: {self.__cab_number} CabColor: {self.__cab_color}'
