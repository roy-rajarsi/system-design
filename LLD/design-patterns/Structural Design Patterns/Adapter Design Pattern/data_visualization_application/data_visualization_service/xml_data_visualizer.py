from .data_visualizer import DataVisualizer


class XMLDataVisualizer(DataVisualizer):

    """ Concrete Implementation of Data Visualization """

    def __init__(self) -> None:
        super().__init__()

    def generate_line_graph(self, xml_data: str) -> None:
        print(f'Generated Line Graph from XML data -> {xml_data}')

    def generate_bar_graph(self, xml_data: str) -> None:
        print(f'Generated Bar Graph from XML data -> {xml_data}')

    def generate_pie_chart(self, xml_data: str) -> None:
        print(f'Generated Pie Chart from XML data -> {xml_data}')
