from data_visualization_service.data_visualizer import DataVisualizer
from data_visualization_service.data_visualization_object_factory import DataVisualizationObjectFactory


def client_code() -> None:

    xml_data: str = 'XML Data sent from Client'

    data_visualizer: DataVisualizer = DataVisualizationObjectFactory.get_data_visualization_object()
    data_visualizer.generate_line_graph(xml_data=xml_data)
    data_visualizer.generate_bar_graph(xml_data=xml_data)
    data_visualizer.generate_pie_chart(xml_data=xml_data)
