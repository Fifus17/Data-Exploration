from rnd.domain.poc.city import AvailableCity
from rnd.rbnb.data_provider import load_rbnb_listing_data


def run_poc():
    df = load_rbnb_listing_data(AvailableCity.NEW_YORK)
    print(df.info())


if __name__ == "__main__":
    run_poc()
