from user.driver import Driver


class DriverMetaData:

    def __init__(self, driver: Driver) -> None:
        self.__driver_id: int = driver.get_user_id()
        self.__driver_name: str = driver.get_username()
        self.__driver_rating: float = driver.get_rating()
        self.__cab_number: str = driver.get_cab_number()
        self.__cab_color: str = driver.get_cab_color()

    def __repr__(self) -> str:
        return f'DriverMetaData(DriverId: {self.__driver_id} DriverName: {self.__driver_name} DriverRating: {self.__driver_rating} CabNumber: {self.__cab_number} CabColor: {self.__cab_color})'
