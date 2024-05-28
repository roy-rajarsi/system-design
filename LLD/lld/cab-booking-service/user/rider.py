from .user import User, UserType


class Rider(User):

    def __init__(self, user_id: int, username: str) -> None:
        super().__init__(user_id=user_id, username=username, user_type=UserType.USER_RIDER)
