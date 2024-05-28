from typing import Optional

from cache_server.cache_eviction_policy import CacheEvictionPolicy
from kv_store import KVStore


class NoneKVStore(KVStore):

    def __init__(self, size: int, eviction_policy: CacheEvictionPolicy) -> None:
        super().__init__(size=size, eviction_policy=eviction_policy)

    def add_key_value_pair(self, key: str, value: str) -> None:
        pass

    def get_value_for_key(self, key: str) -> Optional[str]:
        pass

    def update_value_for_key(self, key: str, value: str) -> None:
        pass

    def delete_key_value_pair(self, key: str) -> None:
        pass
