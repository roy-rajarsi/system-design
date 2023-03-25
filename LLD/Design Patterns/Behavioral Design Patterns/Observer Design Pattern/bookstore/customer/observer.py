from abc import ABC, abstractmethod


class Observer(ABC):
    """ Abstract base class for Observer Classes """

    @abstractmethod
    def notify(self) -> None:
        """ This method is exposed to Observer class for the observer instance to get notified """
        pass
