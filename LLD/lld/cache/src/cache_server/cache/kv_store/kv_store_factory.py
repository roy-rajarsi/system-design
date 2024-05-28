from cache_server.cache_eviction_policy import CacheEvictionPolicy
from kv_store import KVStore
from lfu_kv_store import LFUKVStore
from lru_kv_store import LRUKVStore
from none_kv_store import NoneKVStore

from abc import ABC, abstractmethod
from typing import Dict, Type


class KVStoreFactory(ABC):

    __CACHE_EVICTION_POLICY_TO_KV_STORE: Dict[CacheEvictionPolicy, Type[KVStore]] = {
        CacheEvictionPolicy.CACHE_EVICTION_POLICY_LFU: LFUKVStore,
        CacheEvictionPolicy.CACHE_EVICTION_POLICY_LRU: LRUKVStore,
        CacheEvictionPolicy.CACHE_EVICTION_POLICY_NONE: NoneKVStore
    }

    @staticmethod
    @abstractmethod
    def get_kv_store(eviction_policy: CacheEvictionPolicy) -> Type[KVStore]:
        kv_store: KVStore
        if eviction_policy == CacheEvictionPolicy.CACHE_EVICTION_POLICY_LFU:
            return KVStoreFactory.__CACHE_EVICTION_POLICY_TO_KV_STORE.get(CacheEvictionPolicy.CACHE_EVICTION_POLICY_LFU)

        elif eviction_policy == CacheEvictionPolicy.CACHE_EVICTION_POLICY_LRU:
            return KVStoreFactory.__CACHE_EVICTION_POLICY_TO_KV_STORE.get(CacheEvictionPolicy.CACHE_EVICTION_POLICY_LRU)

        else:
            return KVStoreFactory.__CACHE_EVICTION_POLICY_TO_KV_STORE.get(CacheEvictionPolicy.CACHE_EVICTION_POLICY_NONE)
