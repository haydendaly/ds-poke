from typing import List

from bs4.element import Tag

from src.scrape.markets.market import (Market, MarketBase, PartialListing,
                                       PartialListingDetails, Seller)
from src.shared.browser import CSRBrowser

MERCARI_TIMEOUT = 3


class MercariMarket(MarketBase):
    def __init__(self):
        super().__init__(Market.MERCARI, "https://www.mercari.com/jp")
        self.browser = CSRBrowser()

    def _get_search_url(self, query: str, page: int = 0) -> str:
        q = query.replace(" ", "%20")
        url = f"https://jp.mercari.com/search?keyword={q}&status=on_sale&sort=created_time&order=desc"
        if page > 0:
            url += f"&page_token=v1%3A{page}"
        return url

    def _get_item_url(self, item_id: str) -> str:
        item_id = item_id.split("-")[-1]
        return f"https://jp.mercari.com/item/{item_id}"

    def search(self, query: str, page: int = 0) -> List[PartialListing]:
        url = self._get_search_url(query, page)
        self.browser.get(url, MERCARI_TIMEOUT)
        dom = self.browser.get_dom()

        raw_items = list(
            list(dom.find_all("div", id="item-grid")[0].children)[0].children
        )

        items: List[PartialListing] = []
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

    def get_item_details(self, item_id: str) -> PartialListingDetails:
        url = self._get_item_url(item_id)
        self.browser.get(url, MERCARI_TIMEOUT)
        dom = self.browser.get_dom()

        # TODO(hayden): this code is shit but works
        seller: Seller = {"name": "", "rating": 0.0, "url": None, "sales": None}
        seller_elem = dom.find("a", {"data-location": "item_details:seller_info"})
        if seller_elem and seller_elem.children:
            seller_elem_child = list(seller_elem.children)[0]
            seller = {
                "name": seller_elem_child["name"],
                "url": seller_elem["href"],
                "rating": float(seller_elem_child["score"]),
                "sales": None,
            }

        desc_elem = dom.find("mer-show-more")
        description = list(desc_elem.children)[0].text

        image_elems = dom.find(
            "div", {"data-testid": "vertical-thumbnail-scroll"}
        ).find_all("img")
        image_urls = []
        for image_elem in image_elems:
            image_urls.append(image_elem["src"])

        item: PartialListingDetails = {
            "raw_image_urls": image_urls,
            "description": description,
            "seller": seller,
            "url": url,
        }
        return item
