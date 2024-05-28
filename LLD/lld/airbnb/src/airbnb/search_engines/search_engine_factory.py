from enums.search_engine_types import SearchEngineType
from .search_engine import SearchEngine
from .db_search_listing_engine import DBSearchListingEngine
from .quadtree_listing_search_engine import QuadtreeSearchListingEngine
from .none_search_engine import NoneSearchEngine

from abc import ABC
from logging import getLogger, Logger, WARNING
from typing import Optional, Type

logger: Logger = getLogger(__name__)


class SearchEngineFactory(ABC):

    @staticmethod
    def get_search_engine(search_engine_type: SearchEngineType) -> Optional[Type['SearchEngine']]:
        if search_engine_type == SearchEngineType.SEARCH_ENGINE_DB_SEARCH_LISTING_ENGINE:
            return DBSearchListingEngine
        elif search_engine_type == SearchEngineType.SEARCH_ENGINE_QUADTREE_SEARCH_LISTING_ENGINE:
            return QuadtreeSearchListingEngine
        else:
            logger.log(level=WARNING, msg=f'Parameter :: SearchEngineType -> {search_engine_type} is passed to get_search_engine(search_engine_type) Returned NoneSearchEngine by SearchEngineFactory')
            return NoneSearchEngine
