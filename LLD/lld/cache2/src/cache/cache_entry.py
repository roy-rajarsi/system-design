from datetime import time


class CacheEntry:

    def __init__(self, key: str, value: str, ttl: time) -> None:
        self.__key: str = key
        self.__value: str = value
        self.__ttl: time = ttl

    def get_key(self) -> str:
        return self.__key

    def get_value(self) -> str:
        return self.__value

    def set_key(self, value: str) -> None:
        self.__value = value

    def get_ttl(self) -> time:
        return self.__ttl

    def set_ttl(self, ttl: time) -> None:
        self.__ttl = ttl

    def __repr__(self) -> str:
        return f'CacheEntry(Key={self.__key} Value={self.__value} TTL={self.__ttl}s)'
