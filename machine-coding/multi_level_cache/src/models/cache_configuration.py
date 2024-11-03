from typing import List, override

from cache.cache import Cache
from enums.cache_priority import CachePriority


class CacheConfiguration:

    def __init__(self) -> None:
        self.__cache_list: List[Cache] = list()
        self.__cache_priorities_list: List[CachePriority] = list()

    def add_cache(self, cache: Cache, cache_priority: CachePriority) -> None:
        self.__cache_list.append(cache)
        self.__cache_priorities_list.append(cache_priority)

    def get_cache_list(self) -> List[Cache]:
        return [cache for cache in self.__cache_list]

    def get_cache_priorities_list(self) -> List[CachePriority]:
        return [cache_priority for cache_priority in self.__cache_priorities_list]

    @override
    def __repr__(self) -> str:
        return f'CacheConfiguration \n\t(CacheList: {self.__cache_list} \n\tCachePrioritiesList:{self.__cache_priorities_list})'
