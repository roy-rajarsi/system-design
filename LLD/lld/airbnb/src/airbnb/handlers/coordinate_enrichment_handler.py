from .handler import Handler
from requests.search_listing_request import SearchListingRequest
from responses.coordinates_enriched_search_listing_response import CoordinatesEnrichedSearchListingResponse
from geo.models import City, Region

from logging import getLogger, Logger


logger: Logger = getLogger(__name__)


class CoordinateEnrichmentHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(self, request: SearchListingRequest) -> CoordinatesEnrichedSearchListingResponse:
        city: City = City.objects.get(id=request.get_request_attribute('city'))
        region: Region = Region.objects.get(id=request.get_request_attribute('region'))

        return CoordinatesEnrichedSearchListingResponse(response_payload={
            **request.get_request_payload(),
            'city': city,
            'region': region,
            'city_coordinates': (city.latitude, city.longitude),
            'region_coordinates': (region.latitude, region.longitude)
        })
