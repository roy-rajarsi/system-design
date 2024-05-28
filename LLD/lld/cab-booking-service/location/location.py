from collections import namedtuple
from typing import Type

Location: Type['Location'] = namedtuple('Location', ['longitude', 'latitude'])
