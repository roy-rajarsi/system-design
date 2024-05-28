from listing.models import Listing
from .search_engine import SearchEngine

from django.db import connection
from django.db.models import QuerySet
from logging import Logger, getLogger
from typing import Any, Dict


logger: Logger = getLogger(__name__)


class DBSearchListingEngine(SearchEngine):

    @staticmethod
    def search(request: Dict[str, Any]) -> Dict[str, Any]:
        listings: QuerySet = Listing.objects.filter(state=request.get('state'),
                                                    city=request.get('city'),
                                                    region=request.get('region'),
                                                    is_available_for_booking=True,
                                                    available_from__lte=request.get('tentative_booking_date'),
                                                    price__gte=request.get('price_start_range'),
                                                    price__lte=request.get('price_end_range'),
                                                    ).select_related('region', 'property').select_related('city')

        result: Dict[str, Any] = {'listings': listings}
        logger.info(msg=f'DB Query Performed :: {connection.queries}')

        return result
