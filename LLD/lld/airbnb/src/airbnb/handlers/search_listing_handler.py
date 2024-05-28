from .handler import Handler
from requests.search_engine_enriched_search_listing_request import SearchEngineEnrichedSearchListingRequest
from responses.search_listing_response import SearchListingResponse
from search_engines.search_engine import SearchEngine

from typing import Any, Dict, List, Type


class SearchListingHandler(Handler):

    def handle(self, request: SearchEngineEnrichedSearchListingRequest) -> SearchListingResponse:
        search_engine: Type['SearchEngine'] = request.get_request_attribute(attribute='search_engine')
        listings: List[Dict[str, Any]] = search_engine.search(request=request.get_request_payload())

        return SearchListingResponse(response_payload={
            **request.get_request_payload(),
            'listings': listings
        })
