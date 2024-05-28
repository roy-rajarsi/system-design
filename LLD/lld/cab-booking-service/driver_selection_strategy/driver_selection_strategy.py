from user.driver import Driver

from abc import ABC, abstractmethod
from typing import List


class DriverSelectionStrategy(ABC):

    @abstractmethod
    def get_list_of_drivers(self) -> List[Driver]:
        pass
