from typing import Type

from enums.invalidator_type import InvalidatorType
from invalidators.invalidator import Invalidator
from invalidators.min_heap_invalidator import MinHeapInvalidator


class InvalidatorFactory:

    @staticmethod
    def get_invalidator(invalidator_type: InvalidatorType) -> Type['Invalidator']:
        if invalidator_type is InvalidatorType.MIN_HEAP_INVALIDATOR:
            return MinHeapInvalidator
