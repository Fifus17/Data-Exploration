from typing import Callable

import pandas as pd
import math

listing_transformations: dict[str, Callable[..., None]] = {
    "price": lambda x: (
        x.replace("$", "").replace(",", "")
        if isinstance(x, str)
        else (x if not math.isnan(x) else None)
    ),
    "host_is_superhost": lambda x: x == "t",
    "instant_bookable": lambda x: x == "t",
}


def transform_listings(listings: pd.DataFrame) -> pd.DataFrame:
    listings.dropna(subset=["name"], inplace=True)
    for column, transformation in listing_transformations.items():
        if column in listings.columns:
            listings[column] = listings[column].apply(transformation)
