from data_visualization_service.data_visualizer import DataVisualizer
from advanced_data_visualization_service.advanced_data_visualization_service import AdvancedDataVisualizationService


class AdvancedDataVisualizationAdapter(DataVisualizer):

    def __init__(self) -> None:
        self.__advanced_data_visualization_service: AdvancedDataVisualizationService = AdvancedDataVisualizationService()

    def generate_line_graph(self, xml_data: str) -> None:
        json_data: str = AdvancedDataVisualizationAdapter.__convert_xml_data_to_json_data(xml_data=xml_data)
        self.__advanced_data_visualization_service.generate_advanced_line_graph_from_json(json_data=json_data)

    def generate_bar_graph(self, xml_data: str) -> None:
        json_data: str = AdvancedDataVisualizationAdapter.__convert_xml_data_to_json_data(xml_data=xml_data)
        self.__advanced_data_visualization_service.generate_advanced_bar_graph_from_json(json_data=json_data)

    def generate_pie_chart(self, xml_data: str) -> None:
        json_data: str = AdvancedDataVisualizationAdapter.__convert_xml_data_to_json_data(xml_data=xml_data)
        self.__advanced_data_visualization_service.generate_advanced_pie_chart_from_json(json_data=json_data)

    @staticmethod
    def __convert_xml_data_to_json_data(xml_data: str) -> str:
        print(f"Converting xml data -> {xml_data} to json")
        return "".join(["json_data_", xml_data])
