from typing import Optional


class Singleton:

    __singleton_instance: Optional['Singleton'] = None

    def __init__(self) -> None:
        if Singleton.__singleton_instance is None:
            Singleton.__singleton_instance = self
        else:
            raise Exception('Multiple Attempts to create Singleton Instance \nPlease use Singleton.get_instance() to get Singleton instance')

    @classmethod
    def get_instance(cls) -> 'Singleton':
        if cls.__singleton_instance is None:
            Singleton()
        return cls.__singleton_instance


# Correct Way to get Singleton instance
singleton_instance1: Singleton = Singleton.get_instance()
singleton_instance2: Singleton = Singleton.get_instance()

print(singleton_instance1, singleton_instance2)

print('\n\n\n')
singleton_instance3: Singleton = Singleton()
