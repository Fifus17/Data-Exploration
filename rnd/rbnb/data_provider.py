import pandas as pd
from rnd.domain.poc.city import AvailableCity
import requests
import os
import pandera as pa
from pandera.typing import DataFrame


from rnd.rbnb.transform import transform_listings
from rnd.rbnb.schemas.listing import ListingDataFrame


CITIES_URL: dict[AvailableCity, str] = {
    AvailableCity.NEW_YORK: "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-01-03/data/listings.csv.gz",
    AvailableCity.LONDON: "https://data.insideairbnb.com/united-kingdom/england/london/2024-12-11/data/listings.csv.gz",
    AvailableCity.BARCELONA: "https://data.insideairbnb.com/spain/catalonia/barcelona/2024-12-12/data/listings.csv.gz",
}
DATA_DIR = "./data"


def _city_to_filename(city: AvailableCity) -> str:
    return f"{city.name.lower()}_listings.csv.gz"


@pa.check_types(lazy=True)
def load_rbnb_listing_data(city: AvailableCity) -> DataFrame[ListingDataFrame]:
    city_file_path = f"{DATA_DIR}/{_city_to_filename(city)}"

    if not os.path.exists(city_file_path):
        _fetch_rbnb_data(city)

    df = pd.read_csv(
        city_file_path,
        usecols=[col for col in ListingDataFrame.to_schema().columns if col != "city"],
    )
    transform_listings(df)
    df["city"] = city.name
    return df


def _fetch_rbnb_data(city: AvailableCity) -> None:
    url = CITIES_URL.get(city)
    if not url:
        raise ValueError(
            f"Can't fetch data for {city.name}. No URL found for city: {city}"
        )

    response = requests.get(url, stream=True)
    if response.ok:
        os.makedirs(DATA_DIR, exist_ok=True)
        gz_file_path = f"{DATA_DIR}/{city.name.lower()}_listings.csv.gz"

        with open(gz_file_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(
            f"Failed to fetch data for {city.name}. Status code: {response.status_code}"
        )
