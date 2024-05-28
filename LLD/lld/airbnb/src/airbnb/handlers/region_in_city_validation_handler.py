from exceptions.region_not_in_city_exception import RegionNotInCityException
from .handler import Handler
from requests.coordinates_enriched_search_listing_request import CoordinatesEnrichedSearchListingRequest
from responses.region_in_city_validated_search_listing_response import RegionInCityValidatedSearchListingResponse
from utils.utils import get_normalised_coordinates

from typing import Tuple


class RegionInCityValidationHandler(Handler):

    def __init__(self) -> None:
        super().__init__()

    # TODO
    def handle(self, request: CoordinatesEnrichedSearchListingRequest) -> RegionInCityValidatedSearchListingResponse:
        city_mean_length_in_kms: float = request.get_request_attribute('city').mean_length_in_kms
        city_mean_breadth_in_kms: float = request.get_request_attribute('city').mean_breadth_in_kms

        normalised_city_coordinates: Tuple[float, float] = get_normalised_coordinates(coordinates=request.get_request_attribute('city_coordinates'))
        normalised_region_coordinates: Tuple[float, float] = get_normalised_coordinates(coordinates=request.get_request_attribute('region_coordinates'))

        # extreme_left_longitude_of_city: float = normalised_city_coordinates -

        is_region_in_city: bool = True

        if not is_region_in_city:
            raise RegionNotInCityException

        return RegionInCityValidatedSearchListingResponse(response_payload={
            **request.get_request_payload(),
            'is_region_in_city': is_region_in_city
        })
