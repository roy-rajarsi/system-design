from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SearchEngine(ABC):

    @staticmethod
    @abstractmethod
    def search(request: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
