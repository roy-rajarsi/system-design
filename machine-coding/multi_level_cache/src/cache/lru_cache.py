from typing import Dict, override
from threading import Lock
from time import sleep

from .cache import Cache
from enums.cache_store_type import CacheStoreType
from enums.eviction_policy import EvictionPolicy
from enums.invalidator_type import InvalidatorType
from exceptions.key_not_found_exception import KeyNotFoundException
from exceptions.key_already_in_cache_exception import KeyAlreadyInCacheException
from models.cache_entry import CacheEntry
from utils.data_structures.doubly_linked_list.doubly_linked_list import DoublyLinkedListNode, DoublyLinkedList


class LRUCache[Key, Value](Cache):

    def __init__(self, capacity: int, read_time_in_seconds: int, write_time_in_seconds: int, cache_invalidation_job_run_interval_in_seconds: int = 5, invalidator_type=InvalidatorType.MIN_HEAP_INVALIDATOR) -> None:
        super().__init__(
            capacity=capacity,
            read_time_in_seconds=read_time_in_seconds,
            write_time_in_seconds=write_time_in_seconds,
            eviction_policy=EvictionPolicy.LRU,
            cache_store_type=CacheStoreType.IN_HOUSE,
            cache_invalidation_job_run_interval_in_seconds=cache_invalidation_job_run_interval_in_seconds,
            invalidator_type=invalidator_type
        )
        self.__cache_entry_level_locks: Dict[Key, Lock] = dict()
        self.__cache_store: DoublyLinkedList = DoublyLinkedList()
        self.__key_to_cache_entry_dll_node_dict: Dict[Key, DoublyLinkedListNode] = dict()
        self.get_cache_invalidator_thread().start()

    @override
    def get(self, key: Key) -> CacheEntry:
        if self.__cache_entry_level_locks.get(key, None) is None:
            raise KeyNotFoundException(cache=self, key=key)

        with self.__cache_entry_level_locks.get(key):
            cache_entry_dll_node: DoublyLinkedListNode = self.__key_to_cache_entry_dll_node_dict.get(key)

        with self.get_cache_lock():
            if cache_entry_dll_node.get_data().is_expired():
                self.__cache_store.pop(node=cache_entry_dll_node)
                raise KeyNotFoundException(cache=self, key=key)

            self.__cache_store.pop(node=cache_entry_dll_node)
            self.__cache_store.append(node=cache_entry_dll_node)

        return cache_entry_dll_node.get_data()

    @override
    def post(self, key: Key, value: Value) -> CacheEntry:
        if self.__cache_entry_level_locks.get(key, None) is not None:
            if self.__key_to_cache_entry_dll_node_dict.get(key).get_data().is_expired():
                self.delete(key=key)
            else:
                raise KeyAlreadyInCacheException(cache=self, key=key)

        cache_entry: CacheEntry = CacheEntry(key=key, value=value)
        cache_entry_dll_node: DoublyLinkedListNode = DoublyLinkedListNode(data=cache_entry)
        with self.get_cache_lock():
            cache_entry.set_cache_entry_status_to_live()
            self.__cache_store.append(node=cache_entry_dll_node)
            self.__key_to_cache_entry_dll_node_dict[key] = cache_entry_dll_node
            self.__cache_entry_level_locks[key] = Lock()
        self.get_cache_invalidator().add_cache_entry(cache_entry=cache_entry)
        return cache_entry

    @override
    def patch(self, key: Key, value: Value) -> CacheEntry:
        cache_entry: CacheEntry = self.get(key=key)

        with self.__cache_entry_level_locks.get(key):
            cache_entry.set_value(value=value)

        with self.get_cache_lock():
            cache_entry_dll_node: DoublyLinkedListNode = self.__key_to_cache_entry_dll_node_dict.get(key)
            self.__cache_store.pop(node=cache_entry_dll_node)
            self.__cache_store.append(node=cache_entry_dll_node)
        return cache_entry

    @override
    def delete(self, key: Key) -> CacheEntry:
        self.get(key=key)  # This call ensures the key is present in the Cache Store and has not expired

        with self.get_cache_lock():
            cache_entry_dll_node: DoublyLinkedListNode = self.__key_to_cache_entry_dll_node_dict.get(key)
            self.__cache_store.pop(node=cache_entry_dll_node)
            self.__key_to_cache_entry_dll_node_dict.pop(key)
            self.__cache_entry_level_locks.pop(key)

        cache_entry: CacheEntry = cache_entry_dll_node.get_data()
        cache_entry.set_cache_entry_status_to_expired()
        del cache_entry_dll_node
        return cache_entry

    @override
    def invalidate_expired_cache_entries(self) -> None:
        while True:
            self.get_cache_invalidator().invalidate_expired_cache_entries(cache=self)
            sleep(self.get_cache_invalidation_job_run_interval_in_seconds())
