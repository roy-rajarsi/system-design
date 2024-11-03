from typing import Optional


class DoublyLinkedListNode[T]:

    def __init__(self, data: T, left_node: Optional['DoublyLinkedListNode'] = None, right_node: Optional['DoublyLinkedListNode'] = None) -> None:
        self.data: T = data
        self.left_node: Optional['DoublyLinkedListNode'] = left_node
        self.right_node: Optional['DoublyLinkedListNode'] = right_node

    def get_data(self) -> T:
        return self.data

    def get_left_node(self) -> Optional['DoublyLinkedListNode']:
        return self.left_node

    def get_right_node(self) -> Optional['DoublyLinkedListNode']:
        return self.right_node

    def set_data(self, data: T) -> None:
        self.data = data

    def set_left_node(self, left_node: Optional['DoublyLinkedListNode'] = None) -> None:
        self.left_node = left_node

    def set_right_node(self, right_node: Optional['DoublyLinkedListNode'] = None) -> None:
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'DoublyLinkedListNode(Data={self.get_data()})'


class DoublyLinkedList[T]:

    def __init__(self) -> None:
        self.head: Optional[DoublyLinkedListNode[T]] = None
        self.end: Optional[DoublyLinkedListNode[T]] = None

    def append(self, node: DoublyLinkedListNode[T]) -> None:
        if self.head is None:
            self.head = self.end = node
        else:
            self.end.set_right_node(right_node=node)
            node.set_left_node(left_node=node)
            self.end = node

    def pop(self, node: DoublyLinkedListNode[T]) -> None:
        if node is self.head and node is self.end:
            self.head = self.end = None
        elif node is self.head:
            self.head = self.head.get_right_node()
            self.head.set_left_node()
            node.set_right_node()
        elif node is self.end:
            self.end = self.end.get_left_node()
            self.end.set_right_node()
            node.set_left_node()
        else:
            node.get_left_node().set_right_node(right_node=node.get_right_node())
            node.get_right_node().set_left_node(left_node=node.get_left_node())
            node.set_left_node()
            node.set_right_node()
