from threading import current_thread, Thread, Lock
from time import sleep
from typing import Optional


class Singleton:

    __singleton_instance: Optional['Singleton'] = None
    __singleton_instance_parameters_initialized: bool = False
    __lock: Lock = Lock()

    def __new__(cls, *args, **kwargs) -> None:

        cls.__lock.acquire(blocking=True, timeout=-1)

        print(f'{current_thread().name} is running Critical Section')
        
        if cls.__singleton_instance is None:
            print(f'Creating Singleton Instance')
            cls.__singleton_instance = super().__new__(cls)
            print(f'Singleton Instance Created -> {cls.__singleton_instance}')
        
        cls.__lock.release()

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


def create_singleton_instance(param1: int, param2: int) -> None:
    sleep(5)
    Singleton(param1=param1, param2=param2)

thread1: Thread = Thread(target=create_singleton_instance, args=(10, 20), name='Thread1')
thread2: Thread = Thread(target=create_singleton_instance, args=(100, 200), name='Thread2')

thread1.start()
thread2.start()

thread1.join()
thread2.join()
