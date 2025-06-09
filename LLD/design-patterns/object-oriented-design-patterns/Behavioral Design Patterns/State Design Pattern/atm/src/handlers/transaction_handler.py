from threading import Lock
from typing import Optional, final


@final
class TransactionHandler:
    __lock: Lock = Lock()
    __transaction_handler: Optional['TransactionHandler'] = None
    __transaction_handler_initiated: bool = False

    def __new__(cls, *args, **kwargs) -> 'TransactionHandler':
        if cls.__transaction_handler is None:
            with cls.__lock:
                if cls.__transaction_handler is None:
                    cls.__transaction_handler = super().__new__(cls)
                    cls.__transaction_handler.__init__(*args, **kwargs)
        return cls.__transaction_handler

    def __init__(self, *args, **kwargs) -> None:
        if not self.__class__.__is_transaction_handler_initiated():
            self.__transaction_context: TransactionContext = TransactionContext()
            self.__class__.set_transaction_handled_initiated_to_true()

    @classmethod
    def __is_transaction_handler_initiated(cls) -> bool:
        return cls.__transaction_handler_initiated

    @classmethod
    def set_transaction_handled_initiated_to_true(cls) -> None:
        cls.__transaction_handler_initiated = True
