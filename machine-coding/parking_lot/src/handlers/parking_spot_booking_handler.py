from uuid import UUID
from typing import Optional

from enums.parking_status import ParkingStatus
from .handler import Handler
from parking.parking import Parking
from parking_lot_entities.parking_spot import ParkingSpot
from requests.parking_spot_booking_request import ParkingSpotBookingRequest
from responses.parking_spot_booking_response import ParkingSpotBookingResponse


class ParkingSpotBookingHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: ParkingSpotBookingRequest) -> ParkingSpotBookingResponse:
        ticket_id: Optional[UUID] = None
        parking_spot: Optional[ParkingSpot] = request.get_payload().get('parking_spot')
        if parking_spot is not None:
            ticket_id = Parking(parking_spot=parking_spot, vehicle=request.get_payload().get('vehicle')).get_ticket_id()
            parking_spot.set_parking_status(parking_status=ParkingStatus.PARKED)
        return ParkingSpotBookingResponse(payload={
            **request.get_payload(),
            'ticket_id': ticket_id
        })
