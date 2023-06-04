from typing import Optional, Self

from .bank_account_builder import BankAccountBuilder
from bank_account import BankAccount


class BankAccountBuilderVoterRation(BankAccountBuilder):

    def __init__(self) -> None:
        self.__account_holder_name = None
        self.__bank_branch_name = None
        self.__voter_id = None
        self.__aadhar_id = None
        self.__pan_number = None
        self.__ration_number = None

    def set_account_holder_name(self, account_holder_name: str) -> Self:
        self.__account_holder_name = account_holder_name
        return self

    def set_bank_branch_name(self, bank_branch_name: str) -> Self:
        self.__bank_branch_name = bank_branch_name
        return self

    def set_voter_id(self, voter_id: int) -> Self:
        self.__voter_id = voter_id
        return self

    def set_ration_number(self, ration_number: int) -> Self:
        self.__ration_number = ration_number
        return self

    def set_aadhar_id(self, aadhar_id: int) -> Self:
        return self

    def set_pan_number(self, pan_number: int) -> Self:
        return self

    def get_account_holder_name(self) -> Optional[str]:
        return self.__account_holder_name

    def get_bank_branch_name(self) -> Optional[str]:
        return self.__bank_branch_name

    def get_voter_id(self) -> Optional[int]:
        return self.__voter_id

    def get_aadhar_id(self) -> Optional[int]:
        return self.__aadhar_id

    def get_pan_number(self) -> Optional[int]:
        return self.__pan_number

    def get_ration_number(self) -> Optional[int]:
        return self.__ration_number

    def build(self) -> BankAccount:
        return BankAccount(self)
