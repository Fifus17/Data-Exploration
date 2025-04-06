import osmnx as ox
from geopy.distance import geodesic
import geopandas as gpd
from shapely import Point
from rnd.domain.poc.city import AvailableCity

boundind_boxes = {
    AvailableCity.NEW_YORK: (-74.130433, 40.561213, -73.659107, 40.915591),
    AvailableCity.LONDON: (-0.482052, 51.354767, 0.241346, 51.651014),
}


def get_nearest_subway_distance(
    city_subway_stations: gpd.GeoDataFrame,
    lat: float,
    lon: float,
    row_name: int | str,
    total_rows: int,
    search_radius_m: int = 500,
    fallback_value: float = 1000,
) -> float:
    print(f"Getting nearest subway distance... [{row_name}/{total_rows}]")
    # return _get_nearest_distance(
    #     {"railway": "station", "station": "subway"},
    #     lat,
    #     lon,
    #     search_radius_m,
    #     fallback_value,
    # )
    return _calculate_nearest_subway_distance(city_subway_stations, lat, lon)


def get_subway_stations_within_city(city: AvailableCity) -> gpd.GeoDataFrame:
    city_bbox = boundind_boxes.get(city)
    if not city_bbox:
        raise ValueError(f"No bounding box found for city: {city}")
    tags = {"station": "subway"}
    # tags = {"railway": "station", "station": "subway"}
    gdf = ox.features_from_bbox(city_bbox, tags)
    gdf.info()
    return gdf


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return geodesic((lat1, lon1), (lat2, lon2)).meters


def _calculate_nearest_subway_distance(
    city_subway_stations: gpd.GeoDataFrame, lat: float, lon: float
) -> float:
    city_subway_stations["distance"] = city_subway_stations.apply(
        lambda row: geodesic(
            (lat, lon),
            (
                (
                    row.geometry.y
                    if isinstance(row.geometry, Point)
                    else row.geometry.centroid.y
                ),
                (
                    row.geometry.x
                    if isinstance(row.geometry, Point)
                    else row.geometry.centroid.x
                ),
            ),
        ).meters,
        axis=1,
    )
    return city_subway_stations["distance"].min()


def _get_nearest_distance(
    tags: dict, lat: float, lon: float, search_radius_m=500, fallback_value=1000
) -> float | None:
    center_point = (lat, lon)
    tags = {"railway": "station", "station": "subway"}

    try:
        gdf = ox.features_from_point(center_point, tags, dist=search_radius_m)
        return (
            _calculate_nearest_subway_distance(gdf, lat, lon)
            if not gdf.empty
            else fallback_value
        )

    except Exception as e:
        print(f"Error retrieving closest subway station distance: {e}")
        return fallback_value
