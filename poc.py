from rnd.domain.poc.city import AvailableCity
from rnd.rbnb.data_provider import load_rbnb_listing_data


def run_poc():
    df_ny = load_rbnb_listing_data(AvailableCity.NEW_YORK)
    # print(df_ny.info())
    print(df_ny.head())
    df_london = load_rbnb_listing_data(AvailableCity.LONDON)
    print(df_london.head())


if __name__ == "__main__":
    run_poc()
