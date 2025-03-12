import requests
import gzip
import shutil
import csv
import os

from rnd.domain.poc.city import AvailableCity
from rnd.domain.poc.listing import Listing


class DataFetcherPOC:
    CITIES_URL: dict[AvailableCity, str] = {
        AvailableCity.NEW_YORK: "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-01-03/data/listings.csv.gz",
        AvailableCity.LONDON: "https://data.insideairbnb.com/united-kingdom/england/london/2024-12-11/data/listings.csv.gz",
        AvailableCity.BARCELONA: "https://data.insideairbnb.com/spain/catalonia/barcelona/2024-12-12/data/listings.csv.gz",
        # AvailableCity.SAN_FRANCISCO: "https://data.insideairbnb.com/united-states/ca/san-francisco/2024-12-04/data/listings.csv.gz",
        # AvailableCity.PARIS: "https://data.insideairbnb.com/france/ile-de-france/paris/2024-12-06/data/listings.csv.gz",
        # AvailableCity.BERLIN: "https://data.insideairbnb.com/germany/be/berlin/2024-12-21/data/listings.csv.gz"
    }

    @classmethod
    def fetch_data(cls, city: AvailableCity) -> list[Listing]:
        """Fetches and parses Airbnb data for a given city."""
        url = cls.CITIES_URL[city]
        file_name = f"{city.value}.csv.gz"
        csv_file_name = f"{city.value}.csv"

        response = requests.get(url, stream=True)

        if response.status_code != 200:
            raise Exception(f"Failed to download data: {response.status_code}")

        with open(file_name, "wb") as file:
            file.write(response.content)

        with gzip.open(file_name, "rb") as f_in:
            with open(csv_file_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        listings = []

        with open(csv_file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    listing = Listing(
                        id=int(row["id"]),
                        city=city.value,
                        listing_url=row["listing_url"],
                        name=row["name"],
                        description=row.get("description", ""),
                        host_id=int(row["host_id"]),
                        host_name=row["host_name"],
                        host_is_superhost=row.get("host_is_superhost", "f") == "t",
                        neighbourhood=row["neighbourhood_cleansed"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        property_type=row["property_type"],
                        room_type=row["room_type"],
                        accommodates=int(row["accommodates"]),
                        bathrooms=float(row["bathrooms"]) if row["bathrooms"] else None,
                        bedrooms=int(row["bedrooms"]) if row["bedrooms"] else None,
                        beds=int(row["beds"]) if row["beds"] else None,
                        price=float(row["price"].replace("$", "").replace(",", "")),
                        availability_365=int(row["availability_365"]),
                        number_of_reviews=int(row["number_of_reviews"]),
                        review_scores_rating=float(row["review_scores_rating"]) if row["review_scores_rating"] else None,
                        reviews_per_month=float(row["reviews_per_month"]) if row["reviews_per_month"] else None,
                        instant_bookable=row.get("instant_bookable", "f") == "t",
                    )
                    listings.append(listing)
                except ValueError as e:
                    print(f"Skipping row due to error: {e}")
        
        try:
            os.remove(file_name)
            os.remove(csv_file_name)
            print(f"Deleted temporary files: {file_name} and {csv_file_name}")
        except OSError as e:
            print(f"Error deleting files: {e}")

        return listings


if __name__ == "__main__":
    city = AvailableCity.PARIS
    listings = DataFetcherPOC.fetch_data(city)

    for listing in listings[:5]:
        print(listing)
