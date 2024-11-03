from enum import Enum


class CacheEntryStatus(Enum):

    NOT_LIVE = 'NOT_LIVE'
    LIVE = 'LIVE'
    EXPIRED = 'EXPIRED'
