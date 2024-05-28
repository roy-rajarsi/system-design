from flows.search_listing_flow import SearchListingFlow
from .models import Listing
from enums.search_engine_types import SearchEngineType
from .serializers import ListingSerializer

from dateutil import parser
from django.db.models import QuerySet
from django.http.request import QueryDict
from logging import getLogger, Logger
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from typing import Any, Dict, List, Optional


logger: Logger = getLogger(name=__name__)


class ListingApi(APIView):

    authentication_classes: List[BaseAuthentication] = [BasicAuthentication]
    permission_classes: List[BasePermission] = [IsAuthenticated]

    def get(self, request: Request, listing_id: Optional[int] = None, format: Optional[str] = None) -> Response:

        logger.debug(msg=f'Request -> request.data : {request.data} with listing_id: {listing_id}')

        response_payload: Dict[str, Any] = {'message': str()}
        status: int = HTTP_200_OK

        if listing_id is not None:
            try:
                listing: Optional[Listing] = Listing.objects.get(id=listing_id)
                print()
            except Listing.DoesNotExist as e: # listing.models.Listing.DoesNotExist -> <Model>.DoesNotExist
                print(e, type(e))
                listing = None

            response_payload['message'] = 'Listing Found' if listing is not None else 'Listing is not Found'
            response_payload['listing'] = ListingSerializer(listing).data if listing is not None else None
            status = HTTP_200_OK if listing is not None else HTTP_404_NOT_FOUND

        else:
            def generate_request_payload_from_query_params(query_params: QueryDict) -> Dict[str, Any]:
                return {
                    'city': int(query_params.get('city')),
                    'region': int(query_params.get('region')),
                    'state': int(query_params.get('state')),
                    'tentative_booking_date': parser.parse(query_params.get('tentative_booking_date')),
                    'price_start_range': float(query_params.get('price_start_range')),
                    'price_end_range': float(query_params.get('price_end_range'))
                }

            request: Dict[str, Any] = generate_request_payload_from_query_params(query_params=request.query_params)
            listings: Dict[str, Any] = SearchListingFlow(search_engine_type=SearchEngineType.SEARCH_ENGINE_DB_SEARCH_LISTING_ENGINE).process_request(request=request).get('listings')
            response_payload['listings'] = ListingSerializer(listings, many=True).data

        return Response(data=response_payload, status=status)

    def post(self, request: Request, format: Optional[str] = None) -> Response:

        logger.debug(msg=f'Request -> request.data : {request.data}')

        response_payload: Dict[str, Any] = {'message': str()}
        status: int = HTTP_201_CREATED
        try:
            listing_serializer: ListingSerializer = ListingSerializer(data=request.data)
            listing_serializer.is_valid(raise_exception=True)
            listing: Listing = listing_serializer.save()
            response_payload['message'] = f'Listing(id={listing.id}) is created'
        except ValidationError as validation_error:
            logger.error(msg=validation_error, exc_info=True)
            response_payload['message'] = str(validation_error)
            status = HTTP_400_BAD_REQUEST
        finally:
            return Response(data=response_payload, status=status)

    # def patch(self, request: Request, format: Optional[str] = None) -> Response:
    #     pass
    #
    # def delete(self, request: Request, format: Optional[str] = None) -> Response:
    #     pass

