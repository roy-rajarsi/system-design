from typing import Tuple


class RegionNotInCityException(Exception):

    def __init__(self, city_coordinates: Tuple[float, float], city_dimenssions: Tuple[float, float], region_coordinates: Tuple[float, float]) -> None:
        self.message: str = f'Region(CenterCoordinates: {region_coordinates}) does not lie in City(CenterCoordinates: {city_coordinates} Dimensions: {city_dimenssions})'
        super().__init__(self.message)
