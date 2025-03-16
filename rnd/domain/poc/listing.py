from dataclasses import dataclass


@dataclass(frozen=True)
class Listing:
    id: int
    city: str
    listing_url: str
    name: str
    description: str | None
    host_id: int
    host_name: str
    host_is_superhost: bool
    neighbourhood: str
    latitude: float
    longitude: float
    property_type: str
    room_type: str
    accommodates: int
    bathrooms: float | None
    bedrooms: int | None
    beds: int | None
    price: float
    availability_365: int
    number_of_reviews: int
    review_scores_rating: float | None
    reviews_per_month: float | None
    instant_bookable: bool

    def __repr__(self):
        return (
            f"\nListing ID: {self.id} | {self.name}\n"
            f"URL: {self.listing_url}\n"
            f"Property: {self.property_type} | {self.room_type} | Accommodates {self.accommodates}\n"
            f"Bedrooms: {self.bedrooms or 'N/A'} | Beds: {self.beds or 'N/A'} | Bathrooms: {self.bathrooms or 'N/A'}\n"
            f"Location: {self.city}, {self.neighbourhood} ({self.latitude}, {self.longitude})\n"
            f"Price: ${self.price:.2f} per night\n"
            f"Availability: {self.availability_365} days/year | Instant Book: {'Yes' if self.instant_bookable else 'No'}\n"
            f"Reviews: {self.number_of_reviews} | Rating: {self.review_scores_rating or 'N/A'} | {self.reviews_per_month or 'N/A'} reviews/month\n"
            f"Host: {self.host_name} (ID: {self.host_id}) | Superhost: {'Yes' if self.host_is_superhost else 'No'}"
        )
