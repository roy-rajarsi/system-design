from context.transaction_context import TransactionContext
from enums.transaction_type import TransactionType
from factories.transaction_factory import TransactionFactory
from models.card import Card
from transaction.transaction import Transaction


def main() -> None:
    transaction_context: TransactionContext = TransactionContext()
    while True:
        print("\n========================================================================\n")
        print("Please insert card:")
        card_number: str = input("Card Number: ")
        name: str = input("Name: ")
        expiry_month: int = int(input("Expiry Month: "))
        expiry_year: int = int(input("Expiry Year: "))

        card: Card = Card(card_number=card_number, name=name, expiry_month=expiry_month, expiry_year=expiry_year)
        transaction_context.insert_card(card=card)

        pin: int = int(input("Pin: "))
        transaction_context.authenticate_card(pin=pin)
        print(transaction_context.get_transaction_logs())

        if not transaction_context.get_transaction_logs().get('Card Authenticated', False):
            print("Card Authenticated Failed...")
            transaction_context.reset_transaction_context()
            continue

        transaction_type: TransactionType = TransactionType.get_transaction_type_from_value(int(input("\n\nPlease enter transaction type:\n1 -> Check Balance\n2 -> Deposit Money\n3 -> Withdraw_money\n\n->-> ")))
        if transaction_type is TransactionType.INVALID:
            print("Invalid Transaction Type !")
            continue

        transaction: Transaction

        if transaction_type is transaction_type.BALANCE_CHECK_TRANSACTION:
            transaction = TransactionFactory.get_transaction(transaction_type=transaction_type)(account=transaction_context.get_account())
        elif transaction_type is transaction_type.MONEY_DEPOSIT_TRANSACTION:
            transaction = TransactionFactory.get_transaction(transaction_type=transaction_type)(account=transaction_context.get_account(), money_to_deposit=float(input("Money To Deposit: ")))
        elif transaction_type is transaction_type.MONEY_WITHDRAW_TRANSACTION:
            transaction = TransactionFactory.get_transaction(transaction_type=transaction_type)(account=transaction_context.get_account(), money_to_withdraw=float(input("Money To Withdraw: ")))
        else:
            transaction_context.reset_transaction_context()
            continue

        transaction_context.init_transaction(transaction=transaction)

        transaction_context.authorize_transaction()
        print(transaction_context.get_transaction_logs())
        print(transaction_context.get_transaction_state())

        if not transaction_context.get_transaction_logs().get('Transaction Authorized', False):
            print('Transaction Not Authorized...')
            transaction_context.reset_transaction_context()
            continue

        transaction_context.transact()
        print('Transaction Result: ', transaction_context.get_transaction_logs())
        transaction_context.reset_transaction_context()


if __name__ == '__main__':
    main()
