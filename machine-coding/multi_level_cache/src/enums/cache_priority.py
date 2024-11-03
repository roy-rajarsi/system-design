from enum import Enum


class CachePriority(Enum):

    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P5 = 5
    P6 = 6
    P7 = 7
    P8 = 8
    P_NONE = None

    @classmethod
    def get_priority_from_priority_value(cls, priority_value: int) -> 'CachePriority':
        if priority_value == 1:
            return cls.P1
        elif priority_value == 2:
            return cls.P2
        elif priority_value == 3:
            return cls.P3
        elif priority_value == 4:
            return cls.P4
        elif priority_value == 5:
            return cls.P5
        elif priority_value == 6:
            return cls.P6
        elif priority_value == 7:
            return cls.P7
        elif priority_value == 8:
            return cls.P8
        else:
            return cls.P_NONE

    def __lt__(self, other: 'CachePriority') -> bool:
        if self is self.__class__.P_NONE or other is self.__class__.P_NONE:
            raise Exception('Incompatible Priority Comparisons - P_NONE cant be compared with others')

        return other.value < self.value

    def __gt__(self, other: 'CachePriority') -> bool:
        if self is self.__class__.P_NONE or other is self.__class__.P_NONE:
            raise Exception('Incompatible Priority Comparisons - P_NONE cant be compared with others')

        return other.value > self.value

    def __sub__(self, other: int) -> 'CachePriority':
        if self is self.__class__.P_NONE or other is self.__class__.P_NONE:
            raise Exception('Incompatible Subtraction - P_NONE cant be involved in subtraction')

        return self.__class__.get_priority_from_priority_value(priority_value=self.value - other)
