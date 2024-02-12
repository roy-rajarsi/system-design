from typing import Optional


class Singleton:

    __singleton_instance: Optional['Singleton'] = None
    __singleton_instance_parameters_initialized: bool = False

    def __new__(cls, *args, **kwargs) -> None:

        if cls.__singleton_instance is None:
            print(f'Creating Singleton Instance')
            cls.__singleton_instance = super().__new__(cls)
            print(f'Singleton Instance Created -> {cls.__singleton_instance}')

        return cls.__singleton_instance

    def __init__(self, param1: int = 0, param2: int = 0) -> None:
        if Singleton.__singleton_instance_parameters_initialized:
            
            # If paramters are default paramters then no need to print any warning or raise Exception
            if param1 == 0 and param2 == 0:
                return
            print('WARNING :: Singleton Instance Parameters already initialized. Hence no changes will be reflected')
            return

        self.__param1: int = param1
        self.__param2: int = param2
        Singleton.__singleton_instance_parameters_initialized = True


singleton_instance1: Singleton = Singleton(param1=24, param2=36)
print(singleton_instance1)

singleton_instance2: Singleton = Singleton()
print(singleton_instance2)

singleton_instance3: Singleton = Singleton(param1=240, param2=360)
print(singleton_instance3)
