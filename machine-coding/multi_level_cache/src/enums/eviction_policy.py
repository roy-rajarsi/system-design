from enum import Enum


class EvictionPolicy(Enum):

    FIFO = 'FIFO'
    LIFO = 'LIFO'
    LRU = 'LRU'
    LFU = 'LFU'
    NONE = 'NONE'
