from abc import ABC, abstractmethod
from customer.observer import Observer


class Observable(ABC):
    """ Abstract base class for Observable Classes """

    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        """ Registers an observer to the observer list """
        pass

    @abstractmethod
    def unregister_observer(self, observer: Observer) -> None:
        """ Unregisters an observer from observer list """
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        """ Notifies observers on occurrence of an event"""
        pass

    @abstractmethod
    def is_observer(self, observer: Observer) -> bool:
        """ Returns true/false based on whether an Observer instance is in  """
        pass
