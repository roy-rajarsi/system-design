from user.rider import Rider


class RiderMetaData:

    def __init__(self, rider: Rider) -> None:
        self.__rider_id: int = rider.get_user_id()
        self.__rider_name: str = rider.get_username()
        self.__rider_rating: float = rider.get_rating()

    def __repr__(self) -> str:
        return f'RiderMetaData(RiderId: {self.__rider_id} RiderName: {self.__rider_name} RiderRating: {self.__rider_rating})'
