from store.store import Store
from customer.customer import Customer
import sys
from pathlib import Path


def add_package_to_sys_path() -> None:
    print('Python %s on %s' % (sys.version, sys.platform))
    package_path: str = str(Path(__file__).resolve().parent)
    sys.path.append(package_path)
    print("Package Path -> {package_path} added to python system path".format(package_path=package_path))


def main() -> None:
    add_package_to_sys_path()
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
