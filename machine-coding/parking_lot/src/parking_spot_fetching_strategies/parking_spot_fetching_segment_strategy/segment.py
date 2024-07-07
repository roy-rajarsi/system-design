from typing import Dict, Final, Optional, List

from data_structures.graph import Graph
from parking_lot_entities.entry_gate import EntryGate
from parking_lot_entities.parking_spot import ParkingSpot


class Segment:

    def __init__(self, entry_gate: EntryGate) -> None:
        self.__entry_gate: Final[EntryGate] = entry_gate
        self.__graph: Graph[ParkingSpot] = Graph()
        self.__minimum_distance_from_entry: Dict[ParkingSpot, float] = dict()

    def get_entry_gate(self) -> EntryGate:
        return self.__entry_gate

    def add_parking_spot(self, parking_spot: ParkingSpot) -> None:
        self.__graph.add_node(node=parking_spot)

    def add_distance_between_parking_spots(self, parking_spot1: ParkingSpot, parking_spot2: ParkingSpot, distance: float) -> None:
        self.__graph.add_edge(node1=parking_spot1, node2=parking_spot2, weight=distance)

    def get_parking_spots(self) -> List[ParkingSpot]:
        return self.__graph.get_nodes()

    def compute_minimum_distances_from_entry(self) -> None:
        self.__minimum_distance_from_entry = self.__graph.get_minimum_distance(source_node=self.__entry_gate)

    def get_minimum_distance_from_entry(self, parking_spot: ParkingSpot) -> Optional[float]:
        return self.__minimum_distance_from_entry.get(parking_spot, None)
