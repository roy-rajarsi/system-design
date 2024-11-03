from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cache.cache import Cache
from models.cache_entry import CacheEntry


class Invalidator(ABC):

    @abstractmethod
    def add_cache_entry(self, cache_entry: CacheEntry) -> None:
        pass

    @abstractmethod
    def invalidate_expired_cache_entries(self, cache: Cache) -> None:
        pass
