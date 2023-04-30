from enum import Enum
from typing import List, Optional, TypedDict


class Market(Enum):
    YAHOO_AUCTIONS = "yahoo-auctions"
    MERCARI = "mercari"
    EBAY = "ebay"
    PWCC = "pwcc"


class PartialListing(TypedDict):
    item_id: str
    market: str
    title: str
    thumbnail_url: Optional[str]
    price: Optional[float]


class Seller(TypedDict):
    name: str
    rating: float
    location: Optional[str]
    id: Optional[str]
    sales: Optional[int]


class PartialListingDetails(TypedDict):
    raw_image_urls: List[str]
    description: str
    seller: Seller
    url: str


class Listing(PartialListing, PartialListingDetails):
    image_urls: Optional[List[str]]


class MarketBase:
    def __init__(self, name: Market, url: str):
        self.name = name
        self.url = url

    def search(self, query, page=0) -> List[PartialListing]:
        raise NotImplementedError("search not implemented")

    def get_item_details(self, item_id) -> PartialListingDetails:
        raise NotImplementedError("get_item_details not implemented")
