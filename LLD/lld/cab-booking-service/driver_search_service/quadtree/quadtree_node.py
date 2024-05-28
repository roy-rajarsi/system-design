from location.location import Location
from user.driver import Driver

from collections import namedtuple
from enum import Enum
from typing import List, Optional, Type


Driver_DriverLocation: Type['Driver_DriverLocation'] = namedtuple(typename='Driver_DriverLocation', field_names=['driver', 'driver_location']) # TODO: maintain this as a dict somewhere


class QuadTreeNodeType(Enum):

    QUAD_TREENODE_LEAF_EMPTY = 'QUAD_TREENODE_LEAF_EMPTY'
    QUAD_TREENODE_LEAF_PARTIALLY_FILLED = 'QUAD_TREENODE_LEAF_PARTIALLY_FILLED'
    QUAD_TREENODE_LEAF_FILLED = 'QUAD_TREENODE_LEAF_FILLED'
    QUAD_TREENODE_DIVIDED = 'QUAD_TREENODE_DIVIDED'


class QuadTreeNode:

    def __init__(self, center_location: Location, half_length: float, half_breadth: float, max_driver_count: int, list_of_drivers: Optional[List[Driver_DriverLocation]] = None, parent_quadtree_node: Optional['QuadTreeNode'] = None) -> None:
        self.__center_location: Location = center_location
        self.__half_length: float = half_length
        self.__half_breadth: float = half_breadth
        self.__max_driver_count: int = max_driver_count
        self.__list_of_drivers: List[Driver_DriverLocation] = list_of_drivers if list_of_drivers is not None else list()
        self.__parent_quadtree_node: Optional[QuadTreeNode] = parent_quadtree_node
        self.__north_west_child: Optional[QuadTreeNode] = None
        self.__north_east_child: Optional[QuadTreeNode] = None
        self.__south_west_child: Optional[QuadTreeNode] = None
        self.__south_east_child: Optional[QuadTreeNode] = None
        self.__quadtree_node_type: QuadTreeNodeType = QuadTreeNodeType.QUAD_TREENODE_LEAF_EMPTY

    def get_center_location(self) -> Location:
        return self.__center_location

    def get_half_length(self) -> float:
        return self.__half_length

    def get_half_breadth(self) -> float:
        return self.__half_breadth

    def get_max_driver_count(self) -> int:
        return self.__max_driver_count

    def get_list_of_drivers(self) -> List[Driver_DriverLocation]:
        return self.__list_of_drivers

    def get_parent_quadtree_node(self) -> Optional['QuadTreeNode']:
        return self.__parent_quadtree_node

    def get_north_west_child(self) -> Optional['QuadTreeNode']:
        return self.__north_west_child

    def get_north_east_child(self) -> Optional['QuadTreeNode']:
        return self.__north_east_child

    def get_south_west_child(self) -> Optional['QuadTreeNode']:
        return self.__south_west_child

    def get_south_east_child(self) -> Optional['QuadTreeNode']:
        return self.__south_east_child

    def get_quadtree_node_type(self) -> QuadTreeNodeType:
        return self.__quadtree_node_type

    @staticmethod
    def get_child_quadtree_node_for_a_location(quadtree_node: 'QuadTreeNode', location: Location) -> 'QuadTreeNode':
        if location.longitude > quadtree_node.get_center_location().longitude and location.latitude > quadtree_node.get_center_location().latitude:
            return quadtree_node.get_north_east_child()

        elif location.longitude < quadtree_node.get_center_location().longitude and location.latitude > quadtree_node.get_center_location().latitude:
            return quadtree_node.get_north_west_child()

        elif location.longitude < quadtree_node.get_center_location().longitude and location.latitude < quadtree_node.get_center_location().latitude:
            return quadtree_node.get_south_west_child()

        elif location.longitude > quadtree_node.get_center_location().longitude and location.latitude < quadtree_node.get_center_location().latitude:
            return quadtree_node.get_south_east_child()

    def __set_quadtree_node_type(self) -> None:

        driver_count: int = len(self.get_list_of_drivers())

        if driver_count == 0:
            self.__quadtree_node_type = QuadTreeNodeType.QUAD_TREENODE_LEAF_EMPTY

        elif 0 < driver_count < self.get_max_driver_count():
            self.__quadtree_node_type = QuadTreeNodeType.QUAD_TREENODE_LEAF_PARTIALLY_FILLED

        elif driver_count == self.get_max_driver_count():
            self.__quadtree_node_type = QuadTreeNodeType.QUAD_TREENODE_LEAF_FILLED

        elif driver_count > self.get_max_driver_count():
            self.__quadtree_node_type = QuadTreeNodeType.QUAD_TREENODE_DIVIDED

    def __check_location_in_bounds(self, location: Location) -> bool:

        delta_length: float = abs(self.__center_location.longitude - location.longitude)
        delta_breadth: float = abs(self.__center_location.latitude - location.latitude)

        return delta_length <= self.get_half_length() and delta_breadth <= self.get_half_breadth()

    def __create_partitions(self) -> None:

        self.__north_west_child = QuadTreeNode(center_location=Location(longitude=self.get_center_location().longitude - self.get_half_length()/2,
                                                                        latitude=self.get_center_location().latitude + self.get_half_breadth()/2
                                                                        ),
                                               half_length=self.get_half_length() / 2,
                                               half_breadth=self.get_half_breadth() / 2,
                                               max_driver_count=self.get_max_driver_count(),
                                               parent_quadtree_node=self
                                               )

        self.__north_east_child = QuadTreeNode(center_location=Location(longitude=self.get_center_location().longitude + self.get_half_length() / 2,
                                                                        latitude=self.get_center_location().latitude + self.get_half_breadth() / 2
                                                                        ),
                                               half_length=self.get_half_length() / 2,
                                               half_breadth=self.get_half_breadth() / 2,
                                               max_driver_count=self.get_max_driver_count(),
                                               parent_quadtree_node=self
                                               )

        self.__south_west_child = QuadTreeNode(center_location=Location(longitude=self.get_center_location().longitude - self.get_half_length() / 2,
                                                                        latitude=self.get_center_location().latitude - self.get_half_breadth() / 2
                                                                        ),
                                               half_length=self.get_half_length() / 2,
                                               half_breadth=self.get_half_breadth() / 2,
                                               max_driver_count=self.get_max_driver_count(),
                                               parent_quadtree_node=self
                                               )

        self.__south_east_child = QuadTreeNode(center_location=Location(longitude=self.get_center_location().longitude + self.get_half_length() / 2,
                                                                        latitude=self.get_center_location().latitude - self.get_half_breadth() / 2
                                                                        ),
                                               half_length=self.get_half_length() / 2,
                                               half_breadth=self.get_half_breadth() / 2,
                                               max_driver_count=self.get_max_driver_count(),
                                               parent_quadtree_node=self
                                               )

    def __collapse_partitions(self) -> None:
        self.__north_west_child = None
        self.__north_east_child = None
        self.__south_west_child = None
        self.__south_east_child = None

    def __insert_current_list_of_drivers_into_partitions(self) -> None:

        driver_driver_location: Driver_DriverLocation
        for driver_driver_location in self.__list_of_drivers:

            driver: Driver = driver_driver_location.driver
            driver_location: Location = driver_driver_location.driver_location
            child_quadtree_node_to_insert_driver: QuadTreeNode = QuadTreeNode.get_child_quadtree_node_for_a_location(
                quadtree_node=self, location=driver_location)
            child_quadtree_node_to_insert_driver.insert_driver(driver=driver, driver_location=driver_location)

    def insert_driver(self, driver: Driver, driver_location: Location) -> None:
        if not self.__check_location_in_bounds(location=driver_location):
            raise Exception(f'Driver Location : {driver_location} is not in bounds')

        if self.get_quadtree_node_type() is QuadTreeNodeType.QUAD_TREENODE_LEAF_EMPTY or QuadTreeNodeType.QUAD_TREENODE_LEAF_PARTIALLY_FILLED:
            self.get_list_of_drivers().append(Driver_DriverLocation(driver=driver, driver_location=driver_location))
            self.__set_quadtree_node_type()

        elif self.get_quadtree_node_type() is QuadTreeNodeType.QUAD_TREENODE_LEAF_FILLED:
            self.__create_partitions()
            self.__insert_current_list_of_drivers_into_partitions()
            child_quadtree_node_to_insert_driver: QuadTreeNode = QuadTreeNode.get_child_quadtree_node_for_a_location(
                quadtree_node=self, location=driver_location)
            child_quadtree_node_to_insert_driver.insert_driver(driver=driver, driver_location=driver_location)
            self.get_list_of_drivers().append(Driver_DriverLocation(driver=driver, driver_location=driver_location))
            self.__set_quadtree_node_type()

        elif self.get_quadtree_node_type() is QuadTreeNodeType.QUAD_TREENODE_DIVIDED:
            child_quadtree_node_to_insert_driver: QuadTreeNode = QuadTreeNode.get_child_quadtree_node_for_a_location(
                quadtree_node=self, location=driver_location)
            child_quadtree_node_to_insert_driver.insert_driver(driver=driver, driver_location=driver_location)
            self.get_list_of_drivers().append(Driver_DriverLocation(driver=driver, driver_location=driver_location))
            self.__set_quadtree_node_type()

    def remove_driver(self, driver: Driver) -> None:

        try:
            driver_index: int = self.get_list_of_drivers().index(driver)
        except ValueError as error:
            print(f'{driver} instance not found -> {error}')
            return None

        self.get_list_of_drivers().pop(driver_index)
        self.__set_quadtree_node_type()

        if self.get_quadtree_node_type() is QuadTreeNodeType.QUAD_TREENODE_LEAF_FILLED:
            self.__collapse_partitions()
