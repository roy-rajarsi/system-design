from abc import ABC, abstractmethod
from responses.response import Response


class App(ABC):

    """ Handles UI related tasks """

    def __init__(self, response: Response) -> None:
        self._response: Response = response

    def get_response(self) -> Response:
        return self._response

    @abstractmethod
    def render_ui(self) -> str:
        pass
