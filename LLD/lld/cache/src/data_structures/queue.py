from dll import DLLNode, DoublyLinkedList

from typing import Any, List, Optional


class Queue:

    def __init__(self, max_length: int = 100) -> None:
        self.__dll: DoublyLinkedList = DoublyLinkedList()
        self.__max_length: int = max_length

    def is_full(self) -> bool:
        return self.__dll.get_length() == self.__max_length

    def is_empty(self) -> bool:
        return self.__dll.get_length() == 0

    def enqueue(self, data: Any) -> None:
        if self.is_full():
            raise Exception(f'Queue Overflow Exception. Queue Max Length: {self.__max_length} is already reached !')
        self.__dll.add_node_to_end(dll_node=DLLNode(data=data))

    def dequeue(self) -> Any:
        if self.is_empty():
            raise Exception(f'Queue Underflow Exception. Cannot dequeue as Queue Length is 0')
        return self.__dll.remove_node_from_beginning().get_data()

    def peek_node_from_beginning(self) -> Optional[Any]:
        return None if self.is_empty() else self.__dll.peek_node_from_beginning().get_data()

    def peek_node_from_end(self) -> Optional[Any]:
        return None if self.is_empty() else self.__dll.peek_node_from_end().get_data()

    def __repr__(self) -> str:
        queue: List[Any] = list()
        head: Optional[DLLNode] = self.__dll.peek_node_from_beginning()
        dll_node: DLLNode = head

        while dll_node is not None:
            queue.append(dll_node.get_data())
            queue.append('->')
            dll_node = dll_node.get_next_node()

        return f'Queue({"".join(queue[0:len(queue)-1])})'
