from threading import Lock
from typing import Optional, Tuple

from models.account import Account


class Accounts:
    __lock: Lock = Lock()
    __accounts: Optional['Accounts'] = None
    __accounts_initialised: bool = False

    def __new__(cls, *args, **kwargs) -> 'Accounts':
        if cls.__accounts is None:
            with cls.__lock:
                if cls.__accounts is None:
                    cls.__accounts = super().__new__(cls)
                    cls.__accounts.__init__()
        return cls.__accounts

    def __init__(self) -> None:
        if not self.__class__.__accounts_initialised:
            self.card_number_and_pin_to_account_dict: [Tuple[str, int], Account] = {
                ("ABCD-1234", 1234): Account(account_id="ABCD1234", account_holder_name="ABCD", balance=1000),
                ("EFGH-5678", 5678): Account(account_id="EFGH5678", account_holder_name="EFGH", balance=2000),
            }
            self.__class__.__accounts_initialised = True

    def authenticate(self, card_number: str, pin: int) -> Optional[Account]:
        return self.card_number_and_pin_to_account_dict.get((card_number, pin), None)
