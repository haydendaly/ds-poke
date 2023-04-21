from src.scrape.browser import SSRBrowser
from src.shared.error import NotImplementedError

from .market import Market


class YahooAuctionsMarket(Market):
    def __init__(self):
        super().__init__("Yahoo! Auctions", "http://auctions.yahoo.co.jp/", "ja")
        self.browser = SSRBrowser()

    def _get_search_url(self, query):
        q = query.replace(" ", "+")
        return f"https://auctions.yahoo.co.jp/search/search?p={q}&va=pokemon&fixed=2&exflg=1&b=1&n=100&s1=new&o1=d&mode=2"

    def search(self, query):
        url = self._get_search_url(query)
        dom = self.browser.get(url)
        raw_auctions = dom.find_all("ul", class_="Products__items")[0].children

        auctions = []
        for raw_auction in raw_auctions:
            try:
                auction = list(raw_auction.find_all("a", "Product__imageLink"))[0]
                thumbnail = auction["data-auction-img"]
                full_image = thumbnail.split("?pri")[0]
                auctions.append(
                    {
                        "title": auction["data-auction-title"],
                        "image": full_image,
                        "price": float(auction["data-auction-price"]),
                    }
                )
            except Exception as e:
                print(e)
                pass

        return auctions

    def get_item_details(self, item_id):
        raise NotImplementedError("Yahoo! Auctions does not support item details")
