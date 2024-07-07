from typing import Optional

from .handler import Handler
from parking_lot_entities.parking_spot import ParkingSpot
from parking_spot_fetching_strategies.parking_spot_fetching_segment_strategy.parking_spot_fetching_segment_strategy import ParkingSpotFetchingSegmentStrategy
from requests.parking_spot_fetching_request import ParkingSpotFetchingRequest
from responses.parking_spot_fetching_response import ParkingSpotFetchingResponse


class ParkingSpotFetchingHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: ParkingSpotFetchingRequest) -> ParkingSpotFetchingResponse:
        parking_spot: Optional[ParkingSpot] = ParkingSpotFetchingSegmentStrategy.fetch_parking_spot(entry_gate=request.get_payload().get('entry_gate'))
        return ParkingSpotFetchingResponse(payload={
            **request.get_payload(),
            'parking_spot': parking_spot}
        )
