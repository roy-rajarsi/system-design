from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from handlers.handler import Handler


class ExecutionFlow(ABC):

    def __init__(self, handlers: List[Handler]) -> None:
        self.__handlers: List[Handler] = handlers
        self.__head_Handler: Optional[Handler] = self.__handlers[0] if len(self.__handlers) > 0 else None

    def get_head_handler(self) -> Optional[Handler]:
        return self.__head_Handler

    @abstractmethod
    def define_chain_of_responsibility(self) -> None:
        pass

    @abstractmethod
    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        pass
