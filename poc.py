

from rnd.domain.poc.city import AvailableCity, City, CityFactory
from rnd.domain.poc.listing import Listing
from rnd.infrastructure.data_fetching.poc.data_fetching import DataFetcherPOC


def run_poc():
    city = CityFactory.get_city(AvailableCity.NEW_YORK)
    print(city)
    listings: list[Listing] = DataFetcherPOC.fetch_data(AvailableCity.NEW_YORK)
    for listing in listings[:5]:
        print(listing)



if __name__ == "__main__":
    run_poc()
