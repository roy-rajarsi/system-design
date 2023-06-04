from bank_account import BankAccount
from bank_account_builders.bank_account_builder_aadhar_pan import BankAccountBuilderAadharPan
from bank_account_builders.bank_account_builder_voter_ration import BankAccountBuilderVoterRation
from director import Director


def main() -> None:
    configuration_ronaldo: dict = {
        'account_holder_name': 'Ronaldo',
        'bank_branch_name': 'Madrid',
        'aadhar_id': 7,
        'pan_number': 5
    }
    ronaldo_director: Director = Director(bank_account_builder=BankAccountBuilderAadharPan(),
                                          configuration=configuration_ronaldo)
    ronaldo_bank_account: BankAccount = ronaldo_director.direct_bank_account_build()

    configuration_messi: dict = {
        'account_holder_name': 'Messi',
        'bank_branch_name': 'Barcelona',
        'voter_id': 10,
        'ration_number': 7
    }
    messi_director: Director = Director(bank_account_builder=BankAccountBuilderVoterRation(),
                                        configuration=configuration_messi)
    messi_bank_account: BankAccount = messi_director.direct_bank_account_build()

    print(ronaldo_bank_account)
    print(messi_bank_account)


if __name__ == '__main__':
    main()
