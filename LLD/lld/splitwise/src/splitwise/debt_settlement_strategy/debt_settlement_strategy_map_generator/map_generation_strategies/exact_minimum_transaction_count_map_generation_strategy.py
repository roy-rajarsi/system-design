from expense.services.money import Money
from .map_generation_strategy import MapGenerationStrategy
from amount_owed_in_group_map.amount_owed_in_group_map import AmountOwedInGroupMap
from debt_settlement_strategy.debt_settlement_strategy_map_generator.debt_settlement_map import DebtSettlementMap, MoneyReceiver

from copy import deepcopy
from decimal import Decimal
from typing import List


class ExactMinimumTransactionCountMapGenerationStrategy(MapGenerationStrategy):

    @staticmethod
    def generate_minimum_transaction_count_map(amount_owed_map: AmountOwedInGroupMap) -> DebtSettlementMap:
        minimum_transaction_count_debt_settlement_map: DebtSettlementMap = DebtSettlementMap(debt_settlement_map=dict())
        ExactMinimumTransactionCountMapGenerationStrategy.__generate_minimum_transaction_count_map_util(amount_owed_map=amount_owed_map,
                                                                                                        current_debt_settlement_map=DebtSettlementMap(debt_settlement_map=dict()),
                                                                                                        minimum_transaction_count_debt_settlement_map=minimum_transaction_count_debt_settlement_map)
        return minimum_transaction_count_debt_settlement_map

    @staticmethod
    def __generate_minimum_transaction_count_map_util(amount_owed_map: AmountOwedInGroupMap,
                                                      current_debt_settlement_map: DebtSettlementMap, minimum_transaction_count_debt_settlement_map: DebtSettlementMap,
                                                      current_transaction_count: int = 0, minimum_transaction_count: List[int] = List[float('inf')]) -> None:

        if len(amount_owed_map.get_amount_owed_in_group_map()) == 0:
            if current_transaction_count < minimum_transaction_count[0]:
                minimum_transaction_count_debt_settlement_map = DebtSettlementMap(debt_settlement_map=deepcopy(current_debt_settlement_map.get_debt_settlement_map()))
                minimum_transaction_count[0] = current_transaction_count
            return None

        current_user_id: int
        current_money_owed: Money
        current_user_id, current_money_owed = list(amount_owed_map.get_amount_owed_in_group_map().items())[0]

        user_id: int
        money_owed: Money
        for user_id, money_owed in list(amount_owed_map.get_amount_owed_in_group_map().items())[1:]:

            if ExactMinimumTransactionCountMapGenerationStrategy._is_money_owed(money=current_money_owed):
                if not ExactMinimumTransactionCountMapGenerationStrategy._is_money_owed(money=money_owed):
                    
                    payor_user_id: int = user_id
                    debtor_user_id: int = current_user_id

                    current_debt_settlement_map.add_possible_settlement(debtor_user_id=debtor_user_id, payor_user_id=payor_user_id, money_to_be_transferred=money_owed)
                    amount_owed_map.drop_user_from_amount_owed_in_group_map(user_id=current_user_id)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=user_id, money_owed=Money(amount=Decimal(money_owed.get_amount() + current_money_owed.get_amount()),
                                                                                                   currency=list(amount_owed_map.get_amount_owed_in_group_map().values())[0].get_currency()))

                    ExactMinimumTransactionCountMapGenerationStrategy.__generate_minimum_transaction_count_map_util(amount_owed_map=amount_owed_map,
                                                                                                                    current_debt_settlement_map=current_debt_settlement_map, minimum_transaction_count_debt_settlement_map=minimum_transaction_count_debt_settlement_map,
                                                                                                                    current_transaction_count=current_transaction_count+1, minimum_transaction_count=minimum_transaction_count)

                    current_debt_settlement_map.drop_possible_settlement(debtor_user_id=debtor_user_id)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=current_user_id, money_owed=current_money_owed)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=user_id, money_owed=money_owed)

            else:
                if ExactMinimumTransactionCountMapGenerationStrategy._is_money_owed(money=money_owed):

                    payor_user_id: int = current_user_id
                    debtor_user_id: int = user_id

                    current_debt_settlement_map.add_possible_settlement(debtor_user_id=debtor_user_id, payor_user_id=payor_user_id, money_to_be_transferred=money_owed)
                    amount_owed_map.drop_user_from_amount_owed_in_group_map(user_id=current_user_id)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=user_id, money_owed=Money(amount=Decimal(money_owed.get_amount() + current_money_owed.get_amount()),
                                                                                                   currency=list(amount_owed_map.get_amount_owed_in_group_map().values())[0].get_currency()))

                    ExactMinimumTransactionCountMapGenerationStrategy.__generate_minimum_transaction_count_map_util(amount_owed_map=amount_owed_map,
                                                                                                                    current_debt_settlement_map=current_debt_settlement_map, minimum_transaction_count_debt_settlement_map=minimum_transaction_count_debt_settlement_map,
                                                                                                                    current_transaction_count=current_transaction_count + 1, minimum_transaction_count=minimum_transaction_count)

                    current_debt_settlement_map.drop_possible_settlement(debtor_user_id=debtor_user_id)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=current_user_id, money_owed=current_money_owed)
                    amount_owed_map.set_amount_owed_in_group_map(user_id=user_id, money_owed=money_owed)
