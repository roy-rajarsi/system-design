from store.store import Store
from customer.customer import Customer


def main() -> None:
    store_instance: Store = Store()
    customer_instance1: Customer = Customer(name="Customer1")
    customer_instance2: Customer = Customer(name="Customer2")
    store_instance.register_observer(customer_instance1)
    store_instance.register_observer(customer_instance2)
    store_instance.add_book('Ramayana')
    store_instance.add_book('Mahabharata')
    store_instance.add_book('Gita')
    store_instance.unregister_observer(customer_instance2)


if __name__ == '__main__':
    main()
