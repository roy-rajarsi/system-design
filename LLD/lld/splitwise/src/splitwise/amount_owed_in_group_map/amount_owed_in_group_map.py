from expense.services.money import Money

from typing import Dict


class AmountOwedInGroupMap:

    def __init__(self, amount_owed_in_group_map: Dict[int, Money]):
        self.__amount_owed_in_group_map: Dict[int, Money] = amount_owed_in_group_map

    def get_amount_owed_in_group_map(self) -> Dict[int, Money]:
        return self.__amount_owed_in_group_map

    def set_amount_owed_in_group_map(self, user_id: int, money_owed: Money) -> None:
        if user_id not in self.set_amount_owed_in_group_map():
            raise Exception("User Id not in Amount Owed in Group Map")
        self.__amount_owed_in_group_map[user_id] = money_owed

    def drop_user_from_amount_owed_in_group_map(self, user_id: int) -> None:
        self.__amount_owed_in_group_map.pop(user_id)

    def __repr__(self) -> str:
        return f'str({self.__amount_owed_in_group_map})'
