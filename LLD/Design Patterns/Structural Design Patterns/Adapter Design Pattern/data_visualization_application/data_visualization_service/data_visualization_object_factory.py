from .data_visualizer import DataVisualizer
# from .xml_data_visualizer import XMLDataVisualizer

from advanced_data_visualization_adapter import AdvancedDataVisualizationAdapter


class DataVisualizationObjectFactory:

    """ Acts as Object Factory for Data Visualization """

    @staticmethod
    def get_data_visualization_object() -> DataVisualizer:
        # return XMLDataVisualizer()
        return AdvancedDataVisualizationAdapter()
