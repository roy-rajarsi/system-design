from requests.request import Request
from responses.none_response import NoneResponse
from .search_engine import SearchEngine

from typing import Any, Dict


class NoneSearchEngine(SearchEngine):

    @staticmethod
    def search(request: Request) -> Dict[str, Any]:
        return {}
