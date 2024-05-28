from flows.booking.book_listing_flow import BookListingFlow

from dateutil import parser
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from typing import Any, Dict, List, Optional


class BookingApi(APIView):

    authentication_classes: List[BaseAuthentication] = [BasicAuthentication]
    permission_classes: List[BasePermission] = [IsAuthenticated]

    # def get(self, request: Request, booking_id: Optional[int] = None, format=None) -> Response:
    #     pass

    def post(self, request: Request, format: Optional[str] = None) -> Response:
        response: Dict[str, Any] = BookListingFlow().process_request(request={
            'user': request.user,
            'listing_id': int(request.data.get('listing_id')),
            'order_id': request.data.get('order_id'),
            'payment_id': request.data.get('payment_id'),
            'payment_signature': request.data.get('payment_signature'),
            'booking_start_datetime': parser.parse(request.data.get('booking_start_datetime')),
            'booking_duration': int(request.data.get('booking_duration'))
        })
        return Response(data=response, status=HTTP_201_CREATED)
