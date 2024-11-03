from typing import Type

from cache.cache import Cache
from cache.fifo_cache import FIFOCache
from cache.lifo_cache import LIFOCache
from cache.lru_cache import LRUCache
from cache.lfu_cache import LFUCache
from enums.eviction_policy import EvictionPolicy
from enums.cache_store_type import CacheStoreType


class CacheFactory:

    @staticmethod
    def get_cache(eviction_policy: EvictionPolicy, cache_store_type: CacheStoreType) -> Type[Cache]:
        if cache_store_type is CacheStoreType.IN_HOUSE:
            if eviction_policy is EvictionPolicy.FIFO:
                return FIFOCache
            elif eviction_policy is EvictionPolicy.LIFO:
                return LIFOCache
            elif eviction_policy is EvictionPolicy.LFU:
                return LFUCache
            elif eviction_policy is EvictionPolicy.LRU:
                return LRUCache
        elif cache_store_type is CacheStoreType.REDIS:
            return RedisCache
        elif cache_store_type is CacheStoreType.MEMCACHED:
            return MemCached
