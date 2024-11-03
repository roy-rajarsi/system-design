from copy import deepcopy
from datetime import datetime as DateTime
from typing import Any, Final, Optional

from enums.cache_entry_status import CacheEntryStatus


class CacheEntry:

    def __init__(self, key: str, value: Any, ttl_in_seconds: int = 5) -> None:
        self.__key: Final[str] = key
        self.__value: Any = value
        self.__ttl_in_seconds: Final[int] = ttl_in_seconds
        self.__expires_at: Optional[float] = None
        self.__cache_entry_status: CacheEntryStatus = CacheEntryStatus.NOT_LIVE

    def get_key(self) -> str:
        return self.__key

    def get_value(self) -> Any:
        return deepcopy(self.__value)

    def get_ttl_in_seconds(self) -> int:
        return self.__ttl_in_seconds

    def get_cache_entry_status(self) -> CacheEntryStatus:
        return self.__cache_entry_status

    def set_value(self, value: Any) -> None:
        self.__value = value

    def set_cache_entry_status_to_live(self) -> None:
        self.__expires_at = DateTime.now().timestamp() + self.__ttl_in_seconds
        self.__cache_entry_status = CacheEntryStatus.LIVE

    def set_cache_entry_status_to_expired(self) -> None:
        self.__cache_entry_status = CacheEntryStatus.EXPIRED

    def is_expired(self) -> bool:
        return self.__expires_at >= DateTime.now().timestamp()

    def __repr__(self) -> str:
        return f'CacheEntry(Key: {self.__key}\nVALUE: {self.__value} \nTTL_IN_SECS: {self.__ttl_in_seconds} \nEXPIRES_AT_TIMESTAMP: {self.__expires_at} \nCACHE_ENTRY_STATUS: {self.__cache_entry_status})'
