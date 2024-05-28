from kv_store import KVStore

from typing import override, Optional


class LRUKVStore(KVStore):

    @override
    def get(self, key: str) -> Optional[str]:
        pass

    @override
    def post(self, key: str, value: str) -> None:
        pass

    @override
    def patch(self, key: str, value: str) -> None:
        pass

    @override
    def delete(self, key: str) -> None:
        pass
