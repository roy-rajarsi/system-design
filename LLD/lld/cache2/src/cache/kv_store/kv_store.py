from cache.cache_entry import CacheEntry

from abc import ABC, abstractmethod
from threading import Thread
from typing import Optional


class KVStore(ABC):

    def __init__(self, kv_store) -> None:
        self.__kv_store = kv_store
        self.__ttl_validator: Thread = Thread(target=self._ttl_validator, daemon=True)

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def post(self, cache_entry: CacheEntry) -> None:
        pass

    @abstractmethod
    def patch(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    def _ttl_validator(self) -> None:
        pass
