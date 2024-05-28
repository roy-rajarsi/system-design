from expense.services.money import Money


class SettlementTransaction:

    def __init__(self, payor_user_id: int, debtor_user_id: int, money: Money) -> None:
        self.__payor_user_id: int = pass