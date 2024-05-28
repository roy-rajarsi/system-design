from enums.search_engine_types import SearchEngineType
from .execution_flow import ExecutionFlow
from handlers.handler import Handler
from handlers.coordinate_enrichment_handler import CoordinateEnrichmentHandler
from handlers.region_in_city_validation_handler import RegionInCityValidationHandler
from handlers.search_engine_enrichment_handler import SearchEngineEnrichmentHandler
from handlers.search_listing_handler import SearchListingHandler
from listing.serializers import ListingSerializer
from requests.request import Request
from requests.search_listing_request import SearchListingRequest
from requests.coordinates_enriched_search_listing_request import CoordinatesEnrichedSearchListingRequest
from requests.region_in_city_validated_search_listing_request import RegionInCityValidatedSearchListingRequest
from requests.search_engine_enriched_search_listing_request import SearchEngineEnrichedSearchListingRequest
from responses.response import Response
from responses.coordinates_enriched_search_listing_response import CoordinatesEnrichedSearchListingResponse
from responses.region_in_city_validated_search_listing_response import RegionInCityValidatedSearchListingResponse
from responses.search_engine_enriched_search_listing_response import SearchEngineEnrichedSearchListingResponse
from responses.none_response import NoneResponse
from search_engines.search_engine import SearchEngine
from search_engines.db_search_listing_engine import DBSearchListingEngine

from typing import Any, Dict, Type


class SearchListingFlow(ExecutionFlow):

    def __init__(self, search_engine_type: SearchEngineType) -> None:
        self.__search_engine_type: SearchEngineType = search_engine_type
        self.__default_search_engine: Type[SearchEngine] = DBSearchListingEngine
        super().__init__(list_of_handlers=[
            CoordinateEnrichmentHandler(), RegionInCityValidationHandler(), SearchEngineEnrichmentHandler(), SearchListingHandler()
        ])
        self.set_chain_of_execution()

    def set_chain_of_execution(self) -> None:
        index_: int
        previous_handler: Handler = self.get_head_handler()
        for index_ in range(1, self.get_count_of_handlers()):
            current_handler: Handler = self.get_list_of_handlers()[index_]
            previous_handler.set_next_handler(next_handler=current_handler)
            previous_handler = current_handler

        current_handler = self.head_handler
        while current_handler is not None:
            current_handler = current_handler.get_next_handler()

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        current_handler: Handler = self.get_head_handler()
        response: Response = NoneResponse()
        while current_handler is not None:
            request: Request = self.generate_request_for_head_handler(request_payload=request) if current_handler is self.get_head_handler() \
                else self.generate_request_for_handler(response=response)
            response: Response = current_handler.handle(request=request)
            current_handler = current_handler.get_next_handler()

        return self.generate_response_payload_from_tail_handler(response=response)

    def generate_request_for_head_handler(self, request_payload: Dict[str, Any]) -> SearchListingRequest:
        return SearchListingRequest(request_payload={
            **request_payload,
            'search_engine_type': self.__search_engine_type
        })

    def generate_request_for_handler(self, response: Response) -> Request:
        response_payload: Dict[str, Any] = {**response.get_response_payload()}
        if isinstance(response, CoordinatesEnrichedSearchListingResponse):
            return CoordinatesEnrichedSearchListingRequest(request_payload=response_payload)
        elif isinstance(response, RegionInCityValidatedSearchListingResponse):
            return RegionInCityValidatedSearchListingRequest(request_payload=response_payload)
        elif isinstance(response, SearchEngineEnrichedSearchListingResponse):
            return SearchEngineEnrichedSearchListingRequest(request_payload=response_payload)

    def generate_response_payload_from_tail_handler(self, response: Response) -> Dict[str, Any]:
        return response.get_response_payload().get('listings')
