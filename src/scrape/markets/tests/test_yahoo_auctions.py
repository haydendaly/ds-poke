from src.scrape.browser import SSRBrowser
from src.scrape.markets.yahoo_auctions import YahooAuctionsMarket

# Mock data for testing
mock_search_response = [
    {
        "title": "Sample Auction 1",
        "image": "https://image_1.jpg",
        "price": 50.0,
    },
    {
        "title": "Sample Auction 2",
        "image": "https://image_2.jpg",
        "price": 1.0,
    },
]


class MockRawAuction:
    def __init__(self, auction_data):
        self.auction_data = dict()
        self.auction_data["data-auction-id"] = "123"
        self.auction_data["data-auction-img"] = auction_data["image"] + "?pri"
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
    for i in range(len(search_results)):
        assert search_results[i]["title"] == mock_search_response[i]["title"]
        assert search_results[i]["image"] == mock_search_response[i]["image"]
        assert search_results[i]["price"] == mock_search_response[i]["price"]
