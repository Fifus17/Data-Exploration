import pandera as pa
from pandera.typing import Series

from rnd.domain.poc.city import AvailableCity

from .base import BaseDataFrame


class ListingDataFrame(BaseDataFrame):
    id: Series[int] = pa.Field()
    city: Series[str] = pa.Field(isin=[city.name for city in AvailableCity])
    listing_url: Series[str] = pa.Field()
    name: Series[str] = pa.Field()
    description: Series[str] = pa.Field(nullable=True)
    host_id: Series[int] = pa.Field()
    host_is_superhost: Series[bool] = pa.Field()
    neighbourhood_cleansed: Series[str] = pa.Field()
    latitude: Series[float] = pa.Field()
    longitude: Series[float] = pa.Field()
    property_type: Series[str] = pa.Field()
    room_type: Series[str] = pa.Field()
    accommodates: Series[int] = pa.Field()
    bathrooms: Series[float] = pa.Field(nullable=True)
    bedrooms: Series[float] = pa.Field(nullable=True)
    beds: Series[float] = pa.Field(nullable=True)
    price: Series[float] = pa.Field(nullable=True)
    availability_365: Series[int] = pa.Field()
    number_of_reviews: Series[int] = pa.Field()
    review_scores_rating: Series[float] = pa.Field(nullable=True)
    reviews_per_month: Series[float] = pa.Field(nullable=True)
    instant_bookable: Series[bool] = pa.Field()
