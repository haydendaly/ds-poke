from bs4.element import Tag

from src.scrape.browser import SSRBrowser
from src.shared.error import NotImplementedError

from .market import Market


class YahooAuctionsMarket(Market):
    def __init__(self):
        super().__init__("yahoo-auctions", "http://auctions.yahoo.co.jp/", "ja")
        self.browser = SSRBrowser()

    def _get_search_url(self, query):
        q = query.replace(" ", "+")
        return f"https://auctions.yahoo.co.jp/search/search?p={q}&va=pokemon&fixed=2&exflg=1&b=1&n=100&s1=new&o1=d&mode=2"

    def search(self, query):
        url = self._get_search_url(query)
        dom = self.browser.get(url)
        raw_auctions_container = dom.find_all("ul", class_="Products__items")[0]
        raw_auctions = [
            elem for elem in raw_auctions_container.children if isinstance(elem, Tag)
        ]

        auctions = []
        for raw_auction in raw_auctions:
            try:
                auction = raw_auction.find("a", "Product__imageLink")
                image = auction["data-auction-img"]
                image = image.split("?pri")[0]

                item_id = auction["data-auction-id"]
                title = auction["data-auction-title"]
                price = float(auction["data-auction-price"])

                auction = {
                    "title": title,
                    "image": image,
                    "price": price,
                    "item_id": f"{self.name}-{item_id}",
                }
                auctions.append(auction)
            except Exception as e:
                print(e)

        return auctions

    def get_item_details(self, item_id):
        raise NotImplementedError("Yahoo! Auctions does not support item details yet")
