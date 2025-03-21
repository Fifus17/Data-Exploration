from enum import Enum
from dataclasses import dataclass
import json


class AvailableCity(Enum):
    NEW_YORK = "New York"
    LONDON = "London"
    BARCELONA = "Barcelona"
    # PARIS = "Paris"
    # BERLIN = "Berlin"
    # AMSTERDAM = "Amsterdam"
    # SAN_FRANCISCO = "San Francisco"


@dataclass(frozen=True)
class Landmark:
    name: str
    location: tuple[float, float]
    popularity: float = 100  # from 0 to 100???


@dataclass(frozen=True)
class City:
    name: str
    city_centre: tuple[tuple[float, float]]  # Polygon
    landmarks: tuple[Landmark]


class CityFactory:
    JSON_PATH = "rnd/domain/poc/cities.json"

    @classmethod
    def get_city(cls, city: AvailableCity) -> City:
        cities = cls.__load_cities_from_json()
        return cities[city.value]

    @classmethod
    def __load_cities_from_json(cls) -> dict[str, City]:
        """All data was generated by GPT"""
        with open(cls.JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            cities = {}
            for city_name, city_data in data.items():
                city_centre = tuple(tuple(coord) for coord in city_data["city_centre"])
                landmarks = tuple(
                    Landmark(**landmark) for landmark in city_data["landmarks"]
                )
                cities[city_name] = City(
                    name=city_name, city_centre=city_centre, landmarks=landmarks
                )
        return cities
