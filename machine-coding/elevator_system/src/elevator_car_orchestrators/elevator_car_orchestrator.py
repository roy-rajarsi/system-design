from threading import Lock, Thread
from typing import Dict, final, Final, List, Optional

from enums.request_type import RequestType
from elevator.elevator_car import ElevatorCar
from elevator_car_dispatchers.request_look_ahead_dispatcher import RequestLookAheadDispatcher
from request import Request
from threadpools.request_scheduling_threadpool import RequestSchedulingThreadpool


@final
class ElevatorCarOrchestrator:

    __elevator_car_orchestrator: Optional['ElevatorCarOrchestrator'] = None
    __lock: Lock = Lock()
    __params_initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'ElevatorCarOrchestrator':
        if cls.__get_instance() is None:
            cls.__lock.acquire(blocking=True, timeout=-1)
            if cls.__get_instance() is None:
                cls.__elevator_car_orchestrator = super().__new__(cls)
                cls.__elevator_car_orchestrator.__init__(*args, **kwargs)
            cls.__lock.release()
        return cls.__get_instance()

    @classmethod
    def __get_instance(cls) -> Optional['ElevatorCarOrchestrator']:
        return cls.__elevator_car_orchestrator

    @classmethod
    def __is_params_initialized(cls) -> bool:
        return cls.__params_initialized

    @classmethod
    def __set_params_as_initialized(cls) -> None:
        cls.__params_initialized = True

    def __init__(self, floors_to_serve: List[int], service_zone_id: str, number_of_elevators: int) -> None:
        if not self.__class__.__is_params_initialized():
            self.__floors_to_serve: Final[List[int]] = list(sorted(floors_to_serve))
            self.__min_floor_to_serve: Final[int] = floors_to_serve[0]
            self.__max_floor_to_serve: Final[int] = floors_to_serve[-1]
            self.__service_zone_id: str = service_zone_id
            self.__number_of_elevators: int = number_of_elevators
            self.__elevator_car_cluster: List[ElevatorCar] = self.__generate_elevator_car_cluster()
            self.__elevator_car_to_dispatcher_dict: Dict[ElevatorCar, RequestLookAheadDispatcher] = {elevator_car: RequestLookAheadDispatcher(elevator_car=elevator_car) for elevator_car in self.__elevator_car_cluster}
            self.__elevator_cars_dispatching_threadpool: List[Thread] = [Thread(name=f'ElevatorCar-{elevator_car.get_elevator_car_id()}-DispatchingThread',
                                                                                target=dispatcher.serve()) for elevator_car, dispatcher in self.__elevator_car_to_dispatcher_dict.items()]
            self.__request_scheduling_threadpool: RequestSchedulingThreadpool = RequestSchedulingThreadpool(elevator_car_dispatchers=list(self.__elevator_car_to_dispatcher_dict.values()))
            self.__class__.__set_params_as_initialized()

    def __generate_elevator_car_cluster(self) -> List[ElevatorCar]:
        elevator_car_cluster: List[ElevatorCar] = list()
        elevator_car_id: int
        for elevator_car_id in range(self.__number_of_elevators):
            elevator_car_cluster.append(ElevatorCar(elevator_car_id=f'{self.__service_zone_id}-{str(elevator_car_id)}', floors_to_serve=self.__floors_to_serve))
        return elevator_car_cluster

    def start_serving(self) -> None:
        elevator_car_dispatching_thread: Thread
        for elevator_car_dispatching_thread in self.__elevator_cars_dispatching_threadpool:
            elevator_car_dispatching_thread.start()

        self.__request_scheduling_threadpool.start()

    def schedule_request(self, request: Request) -> None:
        if request.get_request_type() == RequestType.PICKUP_REQUEST:
            elevator_car: ElevatorCar
            for elevator_car in self.__elevator_car_cluster:
                self.__request_scheduling_threadpool.schedule_request(elevator_car_dispatcher=self.__elevator_car_to_dispatcher_dict.get(elevator_car),
                                                                      request=request)
        elif request.get_request_type() == RequestType.DISPATCH_REQUEST:
            self.__request_scheduling_threadpool.schedule_request(elevator_car_dispatcher=self.__elevator_car_to_dispatcher_dict.get(request.get_payload().get('elevator_car')),
                                                                  request=request)

