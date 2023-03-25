from typing import List
from store.observable import Observable
from customer.observer import Observer


class Store(Observable):
    """ Store Concrete class """

    def __init__(self) -> None:
        self.__books: List[str] = list()
        self.__customers: List[Observer] = list()

    def is_observer(self, customer: Observer) -> bool:
        return customer in self.__customers

    def register_observer(self, customer: Observer) -> None:
        if not self.is_observer(customer):
            print("Added Customer {customer}".format(customer=customer))
            self.__customers.append(customer)

    def unregister_observer(self, customer: Observer) -> None:
        if self.is_observer(customer=customer):
            for __index, customer_instance in enumerate(self.__customers):
                if customer_instance is customer:
                    print("Removed Customer {customer}".format(customer=customer))
                    self.__customers.pop(__index)

    def notify_observers(self):
        for customer_instance in self.__customers:
            customer_instance.notify()

    def add_book(self, book: str) -> None:
        """ Notifies observers whenever a new book is added in store """

        if book not in self.__books:
            self.__books.append(book)
            self.notify_observers()
