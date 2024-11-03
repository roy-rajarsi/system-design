from typing import List, Optional


class MinHeap[T]:

	def __init__(self) -> None:
		self.heap: List[T] = list()
		self.length: int = 0

	def add_element(self, element: T) -> None:
		self.heap.append(element)
		self.length += 1
		self.percolate_up()

	def peek(self) -> Optional[T]:
		return None if self.is_empty() else self.heap[0]

	def pop(self) -> Optional[T]:
		if self.is_empty():
			return None
		popped_node: T = self.heap[0]
		self.heap[0] = self.heap[self.length - 1]
		self.heap.pop(-1)
		self.length -= 1
		self.percolate_down()
		return popped_node

	def percolate_up(self) -> None:
		child_index: int = self.length - 1
		while child_index > 0:
			parent_index: int = (child_index - 1) // 2
			min_element: T = min(self.heap[parent_index], self.heap[child_index])
			if min_element is self.heap[parent_index]:
				break
			else:
				self.heap[parent_index], self.heap[child_index] = self.heap[child_index], self.heap[parent_index]
				child_index = parent_index

	def percolate_down(self) -> None:
		parent_index: int = 0
		while True:
			child_index1: int = (2 * parent_index) + 1
			child_index2: int = (2 * parent_index) + 2

			if child_index1 < self.length and child_index2 < self.length:
				min_element: T = min(self.heap[parent_index], self.heap[child_index1], self.heap[child_index2])
				if min_element is self.heap[parent_index]:
					break
				elif min_element is self.heap[child_index1]:
					self.heap[parent_index], self.heap[child_index1] = self.heap[child_index1], self.heap[parent_index]
					parent_index = child_index1
				elif min_element is self.heap[child_index2]:
					self.heap[parent_index], self.heap[child_index2] = self.heap[child_index2], self.heap[parent_index]
					parent_index = child_index2

			elif child_index1 < self.length:
				min_element: T = min(self.heap[parent_index], self.heap[child_index1])
				if min_element is self.heap[parent_index]:
					break
				elif min_element is self.heap[child_index1]:
					self.heap[parent_index], self.heap[child_index1] = self.heap[child_index1], self.heap[parent_index]
					parent_index = child_index1

			else:
				break

	def is_empty(self) -> bool:
		return self.length == 0

	def __repr__(self) -> str:
		return f'MinHeap({self.heap})'
