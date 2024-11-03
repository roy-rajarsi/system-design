from enum import Enum


class CacheStoreType(Enum):

    IN_HOUSE = 'In_House'
    REDIS = 'Redis'
    MEMCACHED = 'Memcached'
    NONE = 'NONE'
