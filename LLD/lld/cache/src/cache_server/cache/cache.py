from cache_server.cache_eviction_policy import CacheEvictionPolicy
from kv_store.kv_store import KVStore, KVStoreEntry
from kv_store.kv_store_factory import KVStoreFactory
from request import Request
from response import Response

from datetime import datetime
from time import sleep
from threading import Thread
from typing import Optional


class Cache:

    def __init__(self, id_: str, size: int, eviction_policy: CacheEvictionPolicy, ttl_based_invalidation_service_run_interval: int = 5) -> None:
        self.__id: str = id_
        self.__size: int = size
        self.__eviction_policy: CacheEvictionPolicy = eviction_policy
        self.__kv_store: KVStore = KVStoreFactory.get_kv_store(eviction_policy=self.__eviction_policy)(size=self.__size, eviction_policy=self.__eviction_policy)
        self.__ttl_based_invalidation_service_run_interval: int = ttl_based_invalidation_service_run_interval
        self.__ttl_based_invalidator_daemon_thread: Thread = Thread(name=f'TTL_Based_InvalidatorDaemonThread_{self.__id}',
                                                                    target=self.run_ttl_based_invalidation_service,
                                                                    kwargs={'service_run_interval': ttl_based_invalidation_service_run_interval},
                                                                    daemon=True)
        self.__ttl_based_invalidator_daemon_thread.start()

    def add_key(self, request: Request) -> Response:
        self.__kv_store.add_key_value_pair(key=request.get_payload().get('key'), value=request.get_payload().get('value'))
        return Response(payload={'message': f'Key-Value Pair {request.get_payload().get("key")}: {request.get_payload().get("value")} is created'},
                        status_code='HTTP_201_CREATED')

    def get_key(self, request: Request) -> Response:
        value: Optional[str] = self.__kv_store.get_value_for_key(key=request.get_payload().get('key'))
        not_found_flag: bool = True if value is None else False
        return Response(payload={'message': f'Value for Key: {request.get_payload().get("key")} is {"not" if not_found_flag else ""} found',
                                 'value': None if not_found_flag else value},
                        status_code='HTTP_404_NOT_FOUND' if not_found_flag else 'HTTP_200_OK')

    def update_key(self, request: Request) -> Response:
        value: Optional[str] = self.__kv_store.get_value_for_key(key=request.get_payload().get('key'))
        if value is None:
            return Response(payload={'message': f'Value for Key {request.get_payload().get("key")} is not found'},
                            status_code='HTTP_404_NOT_FOUND')
        self.__kv_store.update_value_for_key(key=request.get_payload().get('key'), value=request.get_payload().get('value'))
        return Response(payload={'message': f'Value for Key: {request.get_payload().get("key")} is updated to {request.get_payload().get("value")}'},
                        status_code='HTTP_200_OK')

    def delete_key(self, request: Request) -> Response:
        value: Optional[str] = self.__kv_store.get_value_for_key(key=request.get_payload().get('key'))
        if value is None:
            return Response(payload={'message': f'Value for Key {request.get_payload().get("key")} is not found'},
                            status_code='HTTP_404_NOT_FOUND')
        self.__kv_store.delete_key_value_pair(key=request.get_payload().get('key'))
        return Response(payload={'message': f'Key-Value Pair {request.get_payload().get("key")}: {request.get_payload().get("value")} is deleted'})

    def run_ttl_based_invalidation_service(self, **kwargs) -> None:
        service_run_interval: int = kwargs.get('service_run_interval')
        while True:
            sleep(service_run_interval)

            kv_store_entry: KVStoreEntry
            for kv_store_entry in self.__kv_store.get_all_items():
                if datetime.now() >= kv_store_entry.get_expiration_time():
                    self.__kv_store.delete_key_value_pair(key=kv_store_entry.get_key())

    def __repr__(self) -> str:
        return f'Cache(Id: {self.__id} Size: {self.__size})'
