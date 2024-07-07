from abc import ABC
from threading import Lock
from typing import Dict, final, List, Optional, Type

from collections import namedtuple
from data_structures import MinHeap
from enums.parking_status import ParkingStatus
from parking_lot.parking_lot import ParkingLot
from parking_lot_entities.entry_gate import EntryGate
from parking_lot_entities.parking_spot import ParkingSpot
from parking_spot_fetching_strategies.parking_spot_fetching_strategy import ParkingSpotFetchingStrategy
from .segment import Segment


#  TODO: Change this to a Class for Comparison
ParkingSpotAndDistanceFromEntry: Type['ParkingSpotAndDistanceFromEntry'] = namedtuple(typename='ParkingSpotAndDistanceFromEntry',
                                                                                      field_names=['parking_spot', 'distance_from_entry'])


@final
class ParkingSpotFetchingSegmentStrategy(ABC, ParkingSpotFetchingStrategy):

    @staticmethod
    def generate_segment_to_min_heap_dict(segments: List[Segment]) -> Dict[Segment, MinHeap[ParkingSpotAndDistanceFromEntry]]:
        segment_to_min_heap_dict: Dict[Segment, MinHeap[ParkingSpotAndDistanceFromEntry]] = dict()
        segment: Segment
        for segment in segments:
            min_heap_elements: List[ParkingSpotAndDistanceFromEntry] = [ParkingSpotAndDistanceFromEntry(parking_spot=parking_spot,
                                                                                                        distance_from_entry=segment.get_minimum_distance_from_entry(parking_spot=parking_spot))
                                                                        for parking_spot in segment.get_parking_spots()]
            segment_to_min_heap_dict[segment] = MinHeap(elements=min_heap_elements)
        return segment_to_min_heap_dict

    __parking_lot: ParkingLot = ParkingLot()
    __entry_gate_to_segment_dict: Dict[EntryGate, Segment] = {entry_gate: Segment(entry_gate=entry_gate) for entry_gate in __parking_lot.get_entry_gates()}
    __segment_to_min_heap_dict: Dict[Segment, MinHeap[ParkingSpotAndDistanceFromEntry]] = generate_segment_to_min_heap_dict(segments=list(__entry_gate_to_segment_dict.values()))
    __segment_to_lock_dict: Dict[Segment, Lock] = {segment: Lock() for segment in list(__entry_gate_to_segment_dict.values())}

    @staticmethod
    def fetch_parking_spot(entry_gate: EntryGate) -> Optional[ParkingSpot]:
        segment: Segment = ParkingSpotFetchingSegmentStrategy.__entry_gate_to_segment_dict.get(entry_gate)
        lock: Lock = ParkingSpotFetchingSegmentStrategy.__segment_to_lock_dict.get(segment)
        lock.acquire(blocking=True, timeout=-1)
        min_heap: Optional[MinHeap] = ParkingSpotFetchingSegmentStrategy.__segment_to_min_heap_dict.get(segment)
        parking_spot: Optional[ParkingSpot] = min_heap.pop()
        if parking_spot is not None:
            parking_spot.set_parking_status(ParkingStatus.NOT_AVAILABLE)
        lock.release()
        return parking_spot
