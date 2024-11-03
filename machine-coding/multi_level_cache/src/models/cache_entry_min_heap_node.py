from typing import Final

from .cache_entry import CacheEntry


class CacheEntryMinHeapNode:

    def __init__(self, cache_entry: CacheEntry) -> None:
        self.__cache_entry: Final[CacheEntry] = cache_entry

    def get_cache_entry(self) -> CacheEntry:
        return self.__cache_entry

    def __lt__(self, other: 'CacheEntryMinHeapNode') -> bool:
        return self.get_cache_entry().get_ttl_in_seconds() < other.get_cache_entry().get_ttl_in_seconds()

    def __repr__(self) -> str:
        return f'CacheEntryMinHeapNode(CacheEntry: {self.__cache_entry})'
