from typing import Any, Dict, List

from cache.cache import Cache
from enums.cache_priority import CachePriority
from enums.http_status import HttpStatus
from exceptions.key_already_in_cache_exception import KeyAlreadyInCacheException
from exceptions.key_not_found_exception import KeyNotFoundException
from models.cache_configuration import CacheConfiguration
from models.cache_entry import CacheEntry
from monitors.multi_level_cache_monitor import MultiLevelCacheMonitor
from request import Request
from response import Response
from types.kv_generic_types import Key, Value


class MultiLevelCache:

    def __init__(self, cache_configuration: CacheConfiguration) -> None:
        self.caches: List[Cache] = list()  # Caches will be sorted based on the Priority :: Higher Priority -> Lower Priority
        self.cache_to_priority_dict: Dict[Cache, CachePriority] = dict()
        self.priority_to_cache_dict: Dict[CachePriority, Cache] = dict()
        self.min_priority: CachePriority = CachePriority.P_NONE
        self.max_priority: CachePriority = CachePriority.P_NONE
        self.cache_monitor: MultiLevelCacheMonitor = MultiLevelCacheMonitor(read_queue_length=10, write_queue_length=10)
        self.build_cache(cache_configuration=cache_configuration)

    def build_cache(self, cache_configuration: CacheConfiguration) -> None:
        list_of_caches: List[Cache] = cache_configuration.get_cache_list()
        list_of_cache_priorities: List[CachePriority] = cache_configuration.get_cache_priorities_list()

        cache_priority: CachePriority
        cache: Cache
        for cache, cache_priority in zip(list_of_caches, list_of_cache_priorities):
            self.caches.append(cache)
            self.priority_to_cache_dict[cache_priority] = cache
            self.cache_to_priority_dict[cache] = cache_priority
            self.min_priority = min(self.min_priority, cache_priority) if self.min_priority is not CachePriority.P_NONE else cache_priority
            self.max_priority = max(self.max_priority, cache_priority) if self.max_priority is not CachePriority.P_NONE else cache_priority
        self.caches.sort(key=lambda x: self.cache_to_priority_dict.get(x), reverse=True)

    def get(self, request: Request) -> Response:
        if request.get_payload().get('key', str()) is str():
            return Response(payload={'message': 'key attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)

        key: Key = request.get_payload().get('key')
        time_to_read: int = 0
        cache: Cache
        for cache in self.caches:
            try:
                cache_entry: CacheEntry = cache.get(key=key)
                time_to_read += cache.get_read_time_in_seconds()
                time_to_read += self.__update_low_priority_caches(current_priority=self.cache_to_priority_dict.get(cache), cache_entry=cache_entry)
                self.cache_monitor.add_read_time(read_time=time_to_read)
                return Response(payload={'message': f'Key: {key} Value: {cache_entry.get_value()}'}, status=HttpStatus.HTTP_200_OK)
            except KeyNotFoundException:
                time_to_read += cache.get_read_time_in_seconds()

        self.cache_monitor.add_read_time(read_time=time_to_read)
        return Response(payload={'message': f'{key} is not found in cache'}, status=HttpStatus.HTTP_404_NOT_FOUND)

    def post(self, request: Request) -> Response:
        if request.get_payload().get('key', str()) is str():
            return Response(payload={'message': 'key attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        if request.get_payload().get('value', str()) is str():
            return Response(payload={'message': 'value attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        if request.get_payload().get('priority', str()) is str():
            return Response(payload={'message': 'priority attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        key: Key = request.get_payload().get('key')
        value: Value = request.get_payload().get('value')
        priority: CachePriority = CachePriority.get_priority_from_priority_value(priority_value=int(request.get_payload().get('priority')))
        if priority is CachePriority.P_NONE:
            return Response(payload={'message': f'Invalid Priority -> {request.get_payload().get('priority')}'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        if priority < self.min_priority or priority > self.max_priority:
            return Response(payload={'message': f'Priority Out Of Bounds -> {request.get_payload().get('priority')} MinPriority: {self.min_priority} MaxPriority: {self.max_priority}'}, status=HttpStatus.HTTP_400_BAD_REQUEST)

        time_to_write: int = 0
        try:
            cache: Cache = self.priority_to_cache_dict.get(priority)
            cache_entry: CacheEntry = cache.post(key=key, value=value)
            time_to_write += cache.get_write_time_in_seconds()
            time_to_write += self.__update_low_priority_caches(current_priority=priority, cache_entry=cache_entry)
            self.cache_monitor.add_write_time(write_time=time_to_write)
            return Response(payload={'message': f'Key: {key} -> Value: {value} is created'}, status=HttpStatus.HTTP_201_CREATED)
        except KeyAlreadyInCacheException:
            return Response(payload={'message': f'Key: {key} is already in Cache'}, status=HttpStatus.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
        if request.get_payload().get('key', str()) is str():
            return Response(payload={'message': 'key attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        if request.get_payload().get('value', str()) is str():
            return Response(payload={'message': 'value attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)
        key: Key = request.get_payload().get('key')
        value: Value = request.get_payload().get('value')

        time_to_write: int = 0
        cache: Cache
        for cache in self.caches:
            try:
                cache.get(key=key)
                cache_entry: CacheEntry = cache.patch(key=key, value=value)
                time_to_write += cache.get_write_time_in_seconds()
                time_to_write += self.__update_high_priority_caches(current_priority=self.cache_to_priority_dict.get(cache), cache_entry=cache_entry)
                self.cache_monitor.add_write_time(write_time=time_to_write)
                return Response(payload={'message': f'Key: {key} is patched with Value: {value}'}, status=HttpStatus.HTTP_200_OK)
            except KeyNotFoundException:
                time_to_write += cache.get_read_time_in_seconds()

        self.cache_monitor.add_write_time(write_time=time_to_write)
        return Response(payload={'message': f'{key} is not found in cache'}, status=HttpStatus.HTTP_404_NOT_FOUND)

    def delete(self, request: Request) -> Response:
        if request.get_payload().get('key', str()) is str():
            return Response(payload={'message': 'key attribute not found in request payload'}, status=HttpStatus.HTTP_400_BAD_REQUEST)

        key: Key = request.get_payload().get('key')
        cache: Cache
        for cache in self.caches:
            try:
                cache_entry: CacheEntry = cache.get(key=key)
                self.__update_high_priority_caches(current_priority=self.cache_to_priority_dict.get(cache), cache_entry=cache_entry)
                return Response(payload={'message': f'Key: {key} Value: {cache_entry.get_value()}'}, status=HttpStatus.HTTP_200_OK)
            except KeyNotFoundException:
                pass

        return Response(payload={'message': f'{key} is not found in cache'}, status=HttpStatus.HTTP_404_NOT_FOUND)

    def get_usage_status(self) -> Dict[str, Any]:
        usage_status: Dict[str, Any] = dict()
        usage_status['Storage'] = {cache: cache.get_storage_use() for cache in self.caches}
        usage_status['Performance'] = {
            'Mean Read Time': self.cache_monitor.get_mean_of_read_times(),
            'Mean Write Time': self.cache_monitor.get_mean_of_write_times()
        }
        return usage_status

    def __update_high_priority_caches(self, current_priority: CachePriority, cache_entry: CacheEntry) -> int:
        higher_priority: CachePriority = CachePriority.get_priority_from_priority_value(priority_value=current_priority.value - 1)
        time_to_write: int = 0

        while higher_priority < self.max_priority:
            cache: Cache = self.priority_to_cache_dict.get(higher_priority)
            cache.post(key=cache_entry.get_key(), value=cache_entry.get_value())
            higher_priority -= 1
            time_to_write += cache.get_write_time_in_seconds()
        return time_to_write

    def __update_low_priority_caches(self, current_priority: CachePriority, cache_entry: CacheEntry) -> int:
        lower_priority: CachePriority = CachePriority.get_priority_from_priority_value(priority_value=current_priority.value + 1)
        time_to_write: int = 0

        while lower_priority > self.min_priority:
            cache: Cache = self.priority_to_cache_dict.get(lower_priority)
            try:
                cache.post(key=cache_entry.get_key(), value=cache_entry.get_value())
            except KeyAlreadyInCacheException:
                cache.patch(key=cache_entry.get_key(), value=cache_entry.get_value())
            finally:
                time_to_write += cache.get_write_time_in_seconds()
            lower_priority += 1
        return time_to_write
