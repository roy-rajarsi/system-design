from abc import ABC, abstractmethod
from threading import Lock, Thread
from typing import Final
from uuid import UUID, uuid4

from enums.cache_store_type import CacheStoreType
from enums.eviction_policy import EvictionPolicy
from enums.invalidator_type import InvalidatorType
from factories.invalidator_factory import InvalidatorFactory
from invalidators.invalidator import Invalidator
from models.cache_entry import CacheEntry


class Cache[Key, Value](ABC):

    def __init__(self, capacity: int, read_time_in_seconds: int, write_time_in_seconds: int, eviction_policy: EvictionPolicy, cache_store_type: CacheStoreType, cache_invalidation_job_run_interval_in_seconds: int = 5, invalidator_type: InvalidatorType = InvalidatorType.MIN_HEAP_INVALIDATOR) -> None:
        self.__cache_id: Final[UUID] = uuid4()
        self.__current_fill: int = 0
        self.__capacity: Final[int] = capacity
        self.__read_time_in_seconds: Final[int] = read_time_in_seconds
        self.__write_time_in_seconds: Final[int] = write_time_in_seconds
        self.__eviction_policy: Final[EvictionPolicy] = eviction_policy
        self.__cache_store_type: Final[CacheStoreType] = cache_store_type

        self.__cache_invalidator: Final[Invalidator] = InvalidatorFactory.get_invalidator(invalidator_type=invalidator_type)()
        self.__cache_invalidator_thread: Final[Thread] = Thread(name='Invalidator', target=self.invalidate_expired_cache_entries(), daemon=True)
        self.__cache_invalidation_job_run_interval_in_seconds: Final[int] = cache_invalidation_job_run_interval_in_seconds
        self.__cache_lock: Final[Lock] = Lock()

    @abstractmethod
    def get(self, key: Key) -> CacheEntry:
        pass

    @abstractmethod
    def post(self, key: Key, value: Value) -> CacheEntry:
        pass

    @abstractmethod
    def patch(self, key: Key, value: Value) -> CacheEntry:
        pass

    @abstractmethod
    def delete(self, key: Key) -> CacheEntry:
        pass

    @abstractmethod
    def invalidate_expired_cache_entries(self) -> None:
        pass

    def is_empty(self) -> bool:
        return self.__current_fill == 0

    def get_cache_id(self) -> UUID:
        return self.__cache_id

    def get_read_time_in_seconds(self) -> int:
        return self.__read_time_in_seconds

    def get_write_time_in_seconds(self) -> int:
        return self.__write_time_in_seconds

    def get_current_fill(self) -> int:
        return self.__current_fill

    def get_capacity(self) -> int:
        return self.__capacity

    def get_storage_use(self) -> float:
        return self.get_current_fill() / self.get_capacity()

    def get_cache_lock(self) -> Lock:
        return self.__cache_lock

    def get_cache_invalidator(self) -> Invalidator:
        return self.__cache_invalidator

    def get_cache_invalidator_thread(self) -> Thread:
        return self.__cache_invalidator_thread

    def get_cache_invalidation_job_run_interval_in_seconds(self) -> int:
        return self.__cache_invalidation_job_run_interval_in_seconds
