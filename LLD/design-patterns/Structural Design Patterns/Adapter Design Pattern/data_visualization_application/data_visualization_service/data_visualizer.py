from abc import ABC, abstractmethod


class DataVisualizer(ABC):

    """ Abstract Base Class or Interface for Data Visualization """

    @abstractmethod
    def generate_line_graph(self, xml_data: str) -> None:
        pass

    @abstractmethod
    def generate_bar_graph(self, xml_data: str) -> None:
        pass

    @abstractmethod
    def generate_pie_chart(self, xml_data: str) -> None:
        pass
