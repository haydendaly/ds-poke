from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.scrape.markets.market import (Market, MarketBase, PartialListing,
                                       PartialListingDetails, Seller)
from src.shared.browser import SSRBrowser


class YahooAuctionsMarket(MarketBase):
    def __init__(self):
        super().__init__(Market.YAHOO_AUCTIONS, "http://auctions.yahoo.co.jp/")
        self.browser = SSRBrowser()

    def _get_search_url(self, query: str, page: int = 0) -> str:
        q = query.replace(" ", "+")
        # TODO(hayden): add page support
        return f"https://auctions.yahoo.co.jp/search/search?p={q}&va=pokemon&fixed=2&exflg=1&b=1&n=100&s1=new&o1=d&mode=2"

    def _get_item_url(self, item_id: str) -> str:
        item_id = item_id.split("-")[-1]
        return f"https://page.auctions.yahoo.co.jp/jp/auction/{item_id}"

    def search(self, query: str, page: int = 0) -> List[PartialListing]:
        url = self._get_search_url(query, page)
        dom = self.browser.get(url)
        raw_auctions_container = dom.find_all("ul", class_="Products__items")[0]
        raw_auctions = [elem for elem in raw_auctions_container.children]

        auctions: List[PartialListing] = []
        for raw_auction in raw_auctions:
            try:
                auction = raw_auction.find("a", "Product__imageLink")
                image = auction["data-auction-img"]
                image = image.split("?pri")[0]

                item_id = auction["data-auction-id"]
                title = auction["data-auction-title"]
                price = float(auction["data-auction-price"])

                auction: PartialListing = {
                    "title": title,
                    "thumbnail_url": image,
                    "price": price,
                    "item_id": f"{self.name.value}-{item_id}",
                    "market": self.name.value,
                }
                auctions.append(auction)
            except Exception as e:
                print(e)

        return auctions

    def get_item_details(self, item_id: str) -> PartialListingDetails:
        url = self._get_item_url(item_id)
        dom = self.browser.get(url)
        raw_images_container = dom.find_all("ul", class_="ProductImage__images")[0]
        raw_images = raw_images_container.find_all("li", class_="ProductImage__image")

        images = []
        for raw_image in raw_images:
            try:
                image_element = raw_image.find("img")
                image_url = image_element["src"]
                images.append(image_url)
            except Exception as e:
                pass

        raw_description_element = dom.find(
            "div", class_="ProductExplanation__commentBody"
        )
        description = BeautifulSoup(
            raw_description_element.text, "html.parser"
        ).get_text(strip=True)

        raw_seller_element = dom.find("div", class_="Seller")
        seller_name_element = raw_seller_element.find("p", class_="Seller__name")
        seller_name = seller_name_element.get_text(strip=True)
        seller_rating_element = raw_seller_element.find(
            "div", class_="Seller__ratingRatio"
        )
        seller_rating = float(
            seller_rating_element.get_text(strip=True).replace("%", "")
        )
        seller_location_element = raw_seller_element.find(
            "dd", class_="Seller__areaName"
        )
        seller_location = seller_location_element.get_text(strip=True)

        seller: Seller = {
            "name": seller_name,
            "rating": seller_rating,
            "location": seller_location,
            "url": None,
            "sales": None,
        }

        item_details: PartialListingDetails = {
            "raw_image_urls": images,
            "description": description,
            "seller": seller,
            "url": url,
        }

        return item_details
