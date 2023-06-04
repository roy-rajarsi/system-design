from bank_account_builders.bank_account_builder import BankAccountBuilder
from bank_account_builders.bank_account_builder_aadhar_pan import BankAccountBuilderAadharPan
from bank_account_builders.bank_account_builder_voter_ration import BankAccountBuilderVoterRation
from bank_account import BankAccount


class Director:

    __bank_account_builder: BankAccountBuilder

    def __init__(self, bank_account_builder: BankAccountBuilder, configuration: dict) -> None:
        self.__bank_account_builder = bank_account_builder
        self.__configuration = configuration

    def direct_bank_account_build(self) -> BankAccount:
        if isinstance(self.__bank_account_builder, BankAccountBuilderAadharPan):
            return self.direct_bank_account_build_by_aadhar_pan()
        elif isinstance(self.__bank_account_builder, BankAccountBuilderVoterRation):
            return self.direct_bank_account_build_by_voter_ration()
        else:
            print("Hello")

    def direct_bank_account_build_by_aadhar_pan(self) -> BankAccount:
        bank_account: BankAccount = self.__bank_account_builder\
                                    .set_account_holder_name(self.__configuration['account_holder_name'])\
                                    .set_bank_branch_name(self.__configuration['bank_branch_name'])\
                                    .set_aadhar_id(self.__configuration['aadhar_id'])\
                                    .set_pan_number(self.__configuration['pan_number']).build()

        return bank_account

    def direct_bank_account_build_by_voter_ration(self) -> BankAccount:
        bank_account: BankAccount = self.__bank_account_builder \
                                    .set_account_holder_name(self.__configuration['account_holder_name']) \
                                    .set_bank_branch_name(self.__configuration['bank_branch_name']) \
                                    .set_voter_id(self.__configuration['voter_id']) \
                                    .set_ration_number(self.__configuration['ration_number']).build()

        return bank_account
