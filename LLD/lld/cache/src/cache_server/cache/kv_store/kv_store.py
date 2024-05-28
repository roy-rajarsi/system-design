from cache_server.cache_eviction_policy import CacheEvictionPolicy

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


class KVStoreEntry:

    def __init__(self, key: str, value: str, ttl: int) -> None:
        self.__key: str = key
        self.__value: str = value
        self.__ttl: int = ttl
        self.__timestamp: datetime = datetime.now()
        self.__expiration_time: datetime = datetime.now() + timedelta(seconds=self.__ttl)

    def get_key(self) -> str:
        return self.__key

    def get_value(self) -> str:
        return self.__value

    def set_value(self, value: str) -> None:
        self.__value = value

    def get_ttl(self) -> int:
        return self.__ttl

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    def set_timestamp(self, timestamp: datetime) -> None:
        self.__timestamp = timestamp

    def get_expiration_time(self) -> datetime:
        return self.__expiration_time


class KVStore(ABC):

    def __init__(self, size: int, eviction_policy: CacheEvictionPolicy = CacheEvictionPolicy.CACHE_EVICTION_POLICY_LRU) -> None:
        self._size: int = size
        self._eviction_policy: CacheEvictionPolicy = eviction_policy

    @abstractmethod
    def add_key_value_pair(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get_value_for_key(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def update_value_for_key(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete_key_value_pair(self, key: str) -> None:
        pass

    @abstractmethod
    def get_all_items(self) -> List[KVStoreEntry]:
        pass

    def __repr__(self) -> str:
        return f'KVStore(Size={self._size}, EvictionPolicy={self._eviction_policy.value})'
