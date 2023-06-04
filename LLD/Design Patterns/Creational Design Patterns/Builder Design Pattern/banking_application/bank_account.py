from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bank_account_builders.bank_account_builder import BankAccountBuilder


class BankAccount:

    __account_holder_name: Optional[str]
    __bank_branch_name: Optional[str]
    __voter_id: Optional[int]
    __aadhar_id: Optional[int]
    __pan_number: Optional[int]
    __ration_number: Optional[int]

    def __init__(self, bank_account_builder: BankAccountBuilder) -> None:
        self.__account_holder_name = bank_account_builder.get_account_holder_name()
        self.__bank_branch_name = bank_account_builder.get_bank_branch_name()
        self.__voter_id = bank_account_builder.get_voter_id()
        self.__aadhar_id = bank_account_builder.get_aadhar_id()
        self.__pan_number = bank_account_builder.get_pan_number()
        self.__ration_number = bank_account_builder.get_pan_number()

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

    def set_account_holder_name(self, account_holder_name: str) -> None:
        self.__account_holder_name = account_holder_name

    def set_bank_branch_name(self, bank_branch_name: str) -> None:
        self.__bank_branch_name = bank_branch_name

    def set_voter_id(self, voter_id: int) -> None:
        self.__voter_id = voter_id

    def set_aadhar_id(self, aadhar_id: int) -> None:
        self.__aadhar_id = aadhar_id

    def set_pan_number(self, pan_number: int) -> None:
        self.__pan_number = pan_number

    def set_ration_number(self, ration_number: int) -> None:
        self.__ration_number = ration_number

    def __str__(self) -> str:
        return "Account Holder Name -> {}\n\
                Bank Branch Name -> {}\n\
                Voter Id -> {} \n\
                Aadhar Id -> {} \n\
                Pan Number -> {} \n\
                Ration Number -> {}".format(self.__account_holder_name,
                                            self.__bank_branch_name,
                                            self.__voter_id,
                                            self.__aadhar_id,
                                            self.__pan_number,
                                            self.__ration_number)
