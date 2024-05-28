from typing import Any, Optional

class DLLNode:

    def __init__(self, data: Any, previous_node: Optional['DLLNode'] = None, next_node: Optional['DLLNode'] = None) -> None:
        self.__data: Any = data
        self.__previous_node: Optional['DLLNode'] = previous_node
        self.__next_node: Optional['DLLNode'] = next_node

    def get_data(self) -> Any:
        return self.__data

    def get_previous_node(self) -> Optional['DLLNode']:
        return self.__previous_node

    def get_next_node(self) -> Optional['DLLNode']:
        return self.__next_node

    def set_previous_node(self, dll_node: Optional['DLLNode']) -> None:
        self.__previous_node = dll_node

    def set_next_node(self, dll_node: Optional['DLLNode']) -> None:
        self.__next_node = dll_node

    def __repr__(self) -> str:
        return f'DLLNode(Data: {self.get_data()})'


class DoublyLinkedList:

    def __init__(self) -> None:
        self.__head: Optional[DLLNode] = None
        self.__tail: Optional[DLLNode] = None
        self.__length: int = 0

    def is_empty(self) -> bool:
        return self.__length == 0

    def __add_initial_node(self, dll_node: DLLNode) -> None:
        self.__head = self.__tail = dll_node

    def add_node_to_beginning(self, dll_node: Optional['DLLNode']) -> None:
        if self.is_empty():
            self.add_node_to_end(dll_node=dll_node)
        else:
            dll_node.set_next_node(dll_node=self.__head)
            self.__head.set_previous_node(dll_node=dll_node)
            self.__head = dll_node
        self.__length += 1

    def add_node_to_end(self, dll_node: DLLNode) -> None:
        if self.is_empty():
            self.__add_initial_node(dll_node=dll_node)
        else:
            self.__tail.set_next_node(dll_node=dll_node)
            dll_node.set_previous_node(dll_node=self.__tail)
            self.__tail = self.__tail.get_next_node()
        self.__length += 1

    def remove_node_from_beginning(self) -> Optional['DLLNode']:
        if self.is_empty():
            return None

        head_next_node: Optional['DLLNode'] = self.__head.get_next_node()
        self.__head.set_next_node(dll_node=None)
        if head_next_node is not None:
            head_next_node.set_previous_node(dll_node=None)
        popped_node: DLLNode = self.__head
        self.__head = head_next_node
        self.__length -= 1
        return popped_node

    def remove_node_from_end(self) -> Optional['DLLNode']:
        if self.is_empty():
            return None

        tail_previous_node: Optional['DLLNode'] = self.__tail.get_previous_node()
        self.__tail.set_previous_node(dll_node=None)
        if tail_previous_node is not None:
            tail_previous_node.set_next_node(dll_node=None)
        popped_node: DLLNode = self.__tail
        self.__tail = tail_previous_node
        self.__length -= 1
        return popped_node

    def peek_node_from_beginning(self) -> Optional['DLLNode']:
        return None if self.is_empty() else self.__head

    def peek_node_from_end(self) -> Optional['DLLNode']:
        return None if self.is_empty() else self.__tail

    def get_length(self) -> int:
        return self.__length

    def __repr__(self) -> str:
        return f'DLL: Head -> {self.__head} Tail -> {self.__tail}'
