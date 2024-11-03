from datetime import datetime as DateTime
from threading import Lock

from .invalidator import Invalidator
from cache.cache import Cache
from exceptions.key_not_found_exception import KeyNotFoundException
from models.cache_entry import CacheEntry
from models.cache_entry_min_heap_node import CacheEntryMinHeapNode
from utils.data_structures.heap.min_heap import MinHeap


class MinHeapInvalidator(Invalidator):

    def __init__(self) -> None:
        super().__init__()
        self.cache_entry_ttl_min_heap: MinHeap[CacheEntryMinHeapNode] = MinHeap()
        self.invalidator_lock: Lock = Lock()

    def add_cache_entry(self, cache_entry: CacheEntry) -> None:
        with self.invalidator_lock:
            self.cache_entry_ttl_min_heap.add_element(element=CacheEntryMinHeapNode(cache_entry=cache_entry))

    def invalidate_expired_cache_entries(self, cache: Cache) -> None:
        # Cache and the TTL Checker is perfectly in-sync

        while True:
            with cache.get_cache_lock():  # Cache Lock Acquire
                if not self.cache_entry_ttl_min_heap.is_empty() and self.cache_entry_ttl_min_heap.peek().get_cache_entry().get_expires_at() > DateTime.now().timestamp():
                    break
            # Cache Lock Release

            # There are keys with expired TTLs. Hence, acquire Lock on those specific keys
            with self.invalidator_lock:
                expired_cache_entry: CacheEntry = self.cache_entry_ttl_min_heap.pop().get_cache_entry()

            # Locks for keys will be acquired, when we call the delete() of the cache
            try:
                cache.delete(key=expired_cache_entry.get_key())
            except KeyNotFoundException:
                pass
