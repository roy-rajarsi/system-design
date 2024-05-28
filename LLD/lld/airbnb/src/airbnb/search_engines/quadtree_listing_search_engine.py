from requests.request import Request
from responses.response import Response
from .search_engine import SearchEngine


class QuadtreeSearchListingEngine(SearchEngine):

    @staticmethod
    def search(request: Request) -> Response:
        return Response()  # TODO
