from src.scrape.browser import CSRBrowser

from .market import Market

MERCARI_TIMEOUT = 3


class MercariMarket(Market):
    def __init__(self):
        super().__init__("Mercari JP", "https://www.mercari.com/jp", "ja")
        self.browser = CSRBrowser()

    def _get_search_url(self, query):
        q = query.replace(" ", "%20")
        return f"https://jp.mercari.com/search?keyword={q}&status=on_sale&sort=created_time&order=desc"

    def search(self, query):
        url = self._get_search_url(query)
        self.browser.get(url, MERCARI_TIMEOUT)
        dom = self.browser.get_dom()

        raw_items = list(
            list(dom.find_all("div", id="item-grid")[0].children)[0].children
        )

        items = []
        for raw_item in raw_items:
            try:
                item = raw_item.find("mer-item-thumbnail")
                name = item["alt"]
                items.append(
                    {
                        "price": float(item["price"]),
                        "name": name,
                        "image": item["src"].replace(
                            "c!/w=240/thumb", "item/detail/orig"
                        ),
                    }
                )
            except Exception as e:
                pass

        return items

    def get_item_details(self, item):
        pass
