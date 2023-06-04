from abc import ABC, abstractmethod
from typing import Optional, Self

from bank_account import BankAccount


class BankAccountBuilder(ABC):

    __account_holder_name: Optional[str]
    __bank_branch_name: Optional[str]
    __voter_id: Optional[int]
    __aadhar_id: Optional[int]
    __pan_number: Optional[int]
    __ration_number: Optional[int]

    @abstractmethod
    def set_account_holder_name(self, account_holder_name: str) -> Self:
        pass

    @abstractmethod
    def set_bank_branch_name(self, bank_branch_name: str) -> Self:
        pass

    @abstractmethod
    def set_aadhar_id(self, aadhar_id: int) -> Self:
        pass

    @abstractmethod
    def set_pan_number(self, pan_number: int) -> Self:
        pass

    @abstractmethod
    def set_voter_id(self, voter_id: int) -> Self:
       pass

    @abstractmethod
    def set_ration_number(self, ration_number: int) -> Self:
        pass

    @abstractmethod
    def get_account_holder_name(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_bank_branch_name(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_voter_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_aadhar_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_pan_number(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_ration_number(self) -> Optional[int]:
        pass

    @abstractmethod
    def build(self) -> BankAccount:
        pass
