from cache_server.cache.cache import Cache
from request import Request
from response import Response

from typing import Dict, List, Optional, Union


class RequestHandler:

    @staticmethod
    def server_request(request: Dict[str, Union[Request, Dict[str, List[Cache]]]]) -> None:
        pass

    @staticmethod
    def serve_read_request(request: Dict[str, Union[Request, Dict[str, List[Cache]]]]) -> None:
        response_found: bool = False
        value: Optional[str] = None
        read_replica: Cache
        for read_replica in request.get('read_cache_pool'):
            response: Response = read_replica.get_key(request=request.get('request'))
            if response.get_status_code() == 'HTTP_200_OK':
                response_found = True
                if response.get_payload().get('timestamp'):
                    pass


