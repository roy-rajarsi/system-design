from abc import ABC, abstractmethod


class Response(ABC):

    """ Base Class handling responses  """

    @abstractmethod
    def generate_response(self) -> dict:
        pass
