from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cache.cache import Cache

from types.kv_generic_types import Key


class KeyAlreadyInCacheException(Exception):

    def __init__(self, cache: Cache, key: Key) -> None:
        message: str = f'{key} already in Cache_{cache.get_cache_id()}'
        super().__init__(message)
