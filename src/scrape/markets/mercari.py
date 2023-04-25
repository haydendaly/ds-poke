from src.scrape.browser import CSRBrowser

from .market import Market

MERCARI_TIMEOUT = 3


class MercariMarket(Market):
    def __init__(self):
        super().__init__("mercari-jp", "https://www.mercari.com/jp", "ja")
        self.browser = CSRBrowser()

    def _get_search_url(self, query, page=0):
        q = query.replace(" ", "%20")
        url = f"https://jp.mercari.com/search?keyword={q}&status=on_sale&sort=created_time&order=desc"
        if page > 0:
            url += f"&page_token=v1%3A{page}"
        return url

    def _get_item_url(self, item_id):
        item_id = item_id.split("-")[-1]
        return f"https://jp.mercari.com/item/{item_id}"

    def search(self, query, page=0):
        url = self._get_search_url(query, page)
        self.browser.get(url, MERCARI_TIMEOUT)
        dom = self.browser.get_dom()

        raw_items = list(
            list(dom.find_all("div", id="item-grid")[0].children)[0].children
        )

        items = []
        for raw_item in raw_items:
            try:
                thumbnail_elem = raw_item.find("div", class_="merItemThumbnail")
                price_elem = raw_item.find("span", class_="merPrice")

                name = thumbnail_elem["aria-label"]
                price = float(list(price_elem.children)[1].text.replace(",", "", 10))

                image = thumbnail_elem.find("source")["srcset"]
                image = image.replace("c!/w=240/thumb", "item/detail/orig")
                image = image.replace("c!/w=240,f=webp/thumb", "item/detail/orig")

                item_id = image.split("photos/")[1].split("_1.jpg")[0]

                items.append(
                    {
                        "price": price,
                        "title": name,
                        "thumbnail_url": image,
                        "item_id": f"{self.name}-{item_id}",
                        "market": self.name,
                    }
                )
            except Exception as e:
                print(e)

        return items

    def get_item_details(self, item):
        pass
