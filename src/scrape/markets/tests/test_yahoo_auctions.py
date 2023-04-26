from typing import List

from src.scrape.markets import PartialListing, YahooAuctionsMarket
from src.shared.browser import SSRBrowser
from src.shared.json import jsonify

# Mock data for testing
mock_search_response: List[PartialListing] = [
    {
        "title": "Sample Auction 1",
        "thumbnail_url": "https://thumbnail_url_1.jpg",
        "price": 50.0,
        "item_id": "yahoo-auctions-123",
        "market": "yahoo-auctions",
    },
    {
        "title": "Sample Auction 2",
        "thumbnail_url": "https://thumbnail_url_2.jpg",
        "price": 1.0,
        "item_id": "yahoo-auctions-456",
        "market": "yahoo-auctions",
    },
]


class MockRawAuction:
    def __init__(self, auction_data):
        self.auction_data = dict()
        self.auction_data["data-auction-id"] = auction_data["item_id"].split("-")[-1]
        self.auction_data["data-auction-img"] = auction_data["thumbnail_url"] + "?pri"
        self.auction_data["data-auction-title"] = auction_data["title"]
        self.auction_data["data-auction-price"] = str(auction_data["price"])

    def find(self, tag, class_):
        if tag == "a" and class_ == "Product__imageLink":
            return self.auction_data

    def __getitem__(self, key):
        return self.auction_data[key]


class MockDom:
    def __init__(self):
        self.children = [MockRawAuction(auction) for auction in mock_search_response]

    def find_all(self, tag, class_):
        if tag == "ul" and class_ == "Products__items":
            return [self]


class MockSSRBrowser(SSRBrowser):
    def get(self, url):
        dom = MockDom()
        return dom


def test_yahoo_auctions_market_search():
    market = YahooAuctionsMarket()
    market.browser = MockSSRBrowser()
    search_results = market.search("pokemon")

    assert len(search_results) == len(mock_search_response)
    for i, res in enumerate(search_results):
        assert jsonify(res) == jsonify(mock_search_response[i])
