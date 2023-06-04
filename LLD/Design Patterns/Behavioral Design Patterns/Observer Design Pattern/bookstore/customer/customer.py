from customer.observer import Observer


class Customer(Observer):
    """ Customer concrete class """

    def __init__(self, name: str) -> None:
        self.__name: str = name

    def notify(self) -> None:
        print("{customer_name} got notified".format(customer_name=self.__name))
        print("New book got added in book store")

    def __str__(self) -> str:
        return "Customer -> {customer_name}".format(customer_name=self.__name)
