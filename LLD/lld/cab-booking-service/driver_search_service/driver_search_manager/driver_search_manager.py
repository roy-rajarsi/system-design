from location.location import Location
from driver_search_service.quadtree.quadtree import QuadTree
from driver_search_service.quadtree.quadtree_node import QuadTreeNode
from user.driver import Driver

from threading import Lock
from typing import List, Optional


class DriverSearchManager:

    __driver_search_manager_instance: Optional['DriverSearchManager'] = None
    __driver_search_manager_instance_params_initialized: bool = False
    __lock: Lock = Lock()

    def __new__(cls, *args, **kwargs) -> 'DriverSearchManager':

        if cls.__driver_search_manager_instance is None:
            cls.__lock.acquire(blocking=True, timeout=-1)
            cls.__driver_search_manager_instance = super().__new__(cls)
            cls.__lock.release()

        return cls.__driver_search_manager_instance

    @classmethod
    def set_params_initialized_flag(cls) -> None:
        cls.__driver_search_manager_instance_params_initialized = True

    def __init__(self, center_location: Location, half_length: float, half_breadth: float, max_driver_count_in_quadtree_node: int) -> None:

        if DriverSearchManager.__driver_search_manager_instance_params_initialized:
            raise Exception(f'Multiple Attempts to Initiate Singleton Class {self.__class__.__name__}....QuadTree Already Initiated')

        self.__quadtree: QuadTree = QuadTree(center_location=center_location,
                                             half_length=half_length,
                                             half_breadth=half_breadth,
                                             max_driver_count_in_quadtree_node=max_driver_count_in_quadtree_node)

        self.__class__.set_params_initialized_flag()

    def insert_driver_in_search_space(self, driver: Driver, driver_location: Location) -> None:
        self.__quadtree.insert_driver(driver=driver, driver_location=driver_location)

    def remove_driver_from_search_space(self, driver: Driver, driver_location: Location) -> None:
        quadtree_node: QuadTreeNode = self.__quadtree.get_quadtree_node(location=driver_location)
        quadtree_node.remove_driver(driver=driver)

    def get_drivers_for_a_ride_request(self, ride_request_source_location: Location) -> List: # TODO : FIX TYPE
        return self.__quadtree.get_drivers_for_ride_request(ride_request_source_location=ride_request_source_location)

    def shift_driver(self, driver: Driver, source_location: Location, destination_location: Location) -> None:
        source_quadtree_node: QuadTreeNode = self.__quadtree.get_quadtree_node(location=source_location)
        source_quadtree_node.remove_driver(driver=driver)
        self.insert_driver_in_search_space(driver=driver, driver_location=destination_location)
