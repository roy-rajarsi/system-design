from exceptions import LocationNotInBoundException
from location.location import Location
from quadtree_node import Driver_DriverLocation, QuadTreeNode, QuadTreeNodeType
from user.driver import Driver

from typing import List


class QuadTree:

    def __init__(self, center_location: Location, half_length: float, half_breadth: float, max_driver_count_in_quadtree_node: int) -> None:
        self.__root: QuadTreeNode = QuadTreeNode(center_location=center_location,
                                                 half_length=half_length,
                                                 half_breadth=half_breadth,
                                                 max_driver_count=max_driver_count_in_quadtree_node)

    def insert_driver(self, driver: Driver, driver_location: Location) -> None:
        try:
            self.__root.insert_driver(driver=driver, driver_location=driver_location)
        except LocationNotInBoundException as location_not_inbound_exception:
            print(location_not_inbound_exception)

    def get_drivers_for_ride_request(self, ride_request_source_location: Location) -> List[Driver_DriverLocation]:
        source_quadtree_node: QuadTreeNode = self.get_quadtree_node(location=ride_request_source_location)
        return self.__get_drivers_for_ride_request_util(source_quadtree_node=source_quadtree_node)

    def get_quadtree_node(self, location: Location, current_quadtree_node: QuadTreeNode = None) -> QuadTreeNode:
        if current_quadtree_node is None:
            current_quadtree_node = self.__root
            return self.get_quadtree_node(location=location, current_quadtree_node=current_quadtree_node)

        if current_quadtree_node.get_quadtree_node_type() == QuadTreeNodeType.QUAD_TREENODE_DIVIDED:
            child_quadtree_node: QuadTreeNode = QuadTreeNode.get_child_quadtree_node_for_a_location(quadtree_node=current_quadtree_node, location=location)
            return self.get_quadtree_node(location=location, current_quadtree_node=child_quadtree_node)

        return current_quadtree_node

    def __get_drivers_for_ride_request_util(self, source_quadtree_node: QuadTreeNode) -> List[Driver_DriverLocation]:
        list_of_drivers_in_quadtree_node: List[Driver_DriverLocation] = source_quadtree_node.get_list_of_drivers()
        if len(list_of_drivers_in_quadtree_node) > 1:
            return list_of_drivers_in_quadtree_node

        else:
            return self.__get_drivers_for_ride_request_util(source_quadtree_node=source_quadtree_node.get_parent_quadtree_node())
