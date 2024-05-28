from cache.cache import Cache
from cache_eviction_policy import CacheEvictionPolicy
from data_structures.queue import Queue
from workers.worker_thread import WorkerThread
from workers.worker_threadpool import WorkerThreadPool
from request import Request

from dotenv import dotenv_values
from time import sleep
from typing import Dict


class CacheServer:

    def __init__(self, id_: str, size_of_cache: int, eviction_policy: str = 'CACHE_EVICTION_POLICY_LRU', read_replica_count: int = 0, write_replica_count: int = 0) -> None:
        self.__id: str = id_
        self.__size_of_cache: int = size_of_cache
        self.__eviction_policy: CacheEvictionPolicy = CacheEvictionPolicy.CACHE_EVICTION_POLICY_LFU \
            if CacheEvictionPolicy.CACHE_EVICTION_POLICY_LFU.value == eviction_policy \
            else CacheEvictionPolicy.CACHE_EVICTION_POLICY_LRU
        self.__read_replica_count: int = read_replica_count
        self.__write_replica_count: int = write_replica_count
        self.__request_queue: Queue = Queue()
        self.__read_cache_pool: Dict[str, Cache] = CacheServer.__generate_cache_pool(cache_server_id=self.__id,
                                                                                     size_of_cache=self.__size_of_cache,
                                                                                     cache_pool_size=self.__read_replica_count,
                                                                                     eviction_policy=self.__eviction_policy)
        self.__write_cache_pool: Dict[str, Cache] = CacheServer.__generate_cache_pool(cache_server_id=self.__id,
                                                                                      size_of_cache=self.__size_of_cache,
                                                                                      cache_pool_size=self.__write_replica_count,
                                                                                      eviction_policy=self.__eviction_policy)
        self.__thread_pool_worker_count: int = int(dotenv_values(dotenv_path='../.env').get('WORKER_COUNT_IN_CACHE_SERVER_THREAD_POOL'))
        self.__thread_pool: WorkerThreadPool = WorkerThreadPool(name=f'CacheServer_{self.__id}_WorkerThreadPool',
                                                                worker_count=self.__thread_pool_worker_count,
                                                                target_function=self.serve_request) # TODO: RequestHandler.handle_request
        self.serve_request()

    def serve_request(self) -> None:
        while True:
            if not self.__request_queue.is_empty():
                request: Request = self.__request_queue.dequeue()
                key: str = request.get_payload().get('key')
                hash_value_of_key: int = hash(key) % self.__thread_pool_worker_count
                worker_thread: WorkerThread = self.__thread_pool.get_worker_thread_for_a_hash_value(hash_value=hash_value_of_key)
                worker_thread.get_task_queue().enqueue(data={'request': request,
                                                             'read_cache_pool': self.__read_cache_pool,
                                                             'write_cache_pool': self.__write_cache_pool})
            else:
                sleep(5)

    @staticmethod
    def __generate_cache_pool(cache_server_id: str, size_of_cache: int, cache_pool_size: int, eviction_policy: CacheEvictionPolicy) -> Dict[str, Cache]:
        cache_pool: Dict[str, Cache] = dict()
        ttl_based_invalidation_service_run_interval: int = int(dotenv_values(dotenv_path="../.env").get("TTL_BASED_INVALIDATION_SERVICE_RUN_INTERVAL"))

        id_: int
        for id_ in range(cache_pool_size):
            cache_id: str = f'CacheServer_{cache_server_id}_Cache_{id_}'
            cache_pool[cache_id] = (Cache(id_=cache_id,
                                    size=size_of_cache,
                                    eviction_policy=eviction_policy,
                                    ttl_based_invalidation_service_run_interval=ttl_based_invalidation_service_run_interval))

        return cache_pool
