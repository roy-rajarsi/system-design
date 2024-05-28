from enums.search_engine_types import SearchEngineType
from .handler import Handler
from requests.region_in_city_validated_search_listing_request import RegionInCityValidatedSearchListingRequest
from responses.search_engine_enriched_search_listing_response import SearchEngineEnrichedSearchListingResponse
from search_engines.search_engine import SearchEngine
from search_engines.search_engine_factory import SearchEngineFactory

from typing import Type


class SearchEngineEnrichmentHandler(Handler):

    def handle(self, request: RegionInCityValidatedSearchListingRequest) -> SearchEngineEnrichedSearchListingResponse:
        search_engine_type: SearchEngineType = request.get_request_attribute(attribute='search_engine_type')
        search_engine: Type['SearchEngine'] = SearchEngineFactory.get_search_engine(search_engine_type=search_engine_type)
        return SearchEngineEnrichedSearchListingResponse(response_payload={
            **request.get_request_payload(),
            'search_engine': search_engine
        })
