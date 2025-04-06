from typing import Callable
import pandas as pd

from rnd.domain.poc.city import AvailableCity
from rnd.rbnb.geospatial_features.shortest_distance import (
    calculate_distance,
    get_nearest_subway_distance,
    get_subway_stations_within_city,
)
from .landmarks.new_york import landmarks as new_york_landmarks
from .landmarks.london import landmarks as london_landmarks
from functools import wraps

landmarks = {
    AvailableCity.NEW_YORK: new_york_landmarks,
    AvailableCity.LONDON: london_landmarks,
}


def add_geospatial_features(
    func: Callable[[AvailableCity], pd.DataFrame],
) -> Callable[[AvailableCity], pd.DataFrame]:
    @wraps(func)
    def wrapper(city: AvailableCity) -> pd.DataFrame:
        df = func(city)
        add_landmark_distances(df, city)
        # add_custom_distances(df, city)
        return df

    return wrapper


def add_landmark_distances(df: pd.DataFrame, city: AvailableCity) -> None:
    if not (city_landmarks := landmarks.get(city)):
        raise ValueError(f"No landmarks available for city: {city}")

    print(f"Adding geospatial features for {city.name} dataset...")
    for i, landmark in enumerate(city_landmarks):
        df[f"dist_{_sanitize_landmark_name(landmark["name"])}"] = df.apply(
            lambda row: calculate_distance(
                row["latitude"],
                row["longitude"],
                landmark["latitude"],
                landmark["longitude"],
            ),
            axis=1,
        )
        print(
            f"Added distance to landmark: {landmark['name']} [{i+1}/{len(city_landmarks)}]"
        )


def add_custom_distances(df: pd.DataFrame, city: AvailableCity) -> None:
    city_subway_stations = get_subway_stations_within_city(city)
    print("Number of subway stations in city bbox:", len(city_subway_stations))
    df["nearest_subway_distance"] = df.apply(
        lambda row: get_nearest_subway_distance(
            city_subway_stations, row["latitude"], row["longitude"], row.name, len(df)
        ),
        axis=1,
    )


def _sanitize_landmark_name(landmark_name: str) -> str:
    shortened_version = [
        f"{word[0].upper()}{word[1:3]}"
        for word in landmark_name.lower().replace("-", "_").split(" ")
    ]
    return "".join(shortened_version)
