import os

from ebaysdk.finding import Connection as Finding

from src.scrape.markets.market import Market, MarketBase

EBAY_APP_ID = os.environ.get("EBAY_APP_ID")


# TODO(hayden): should do this as a webscraper instead of using the API
class eBay(MarketBase):
    def __init__(self):
        super().__init__(Market.EBAY, "https://ebay.com/")
        raise NotImplementedError("eBay does not support search yet")
        self.api = Finding(appid=EBAY_APP_ID, config_file=None)

    def search(self, query):
        raise NotImplementedError("eBay does not support search yet")

        sort_order = "StartTimeNewest"
        itemFilters = [{"name": "ListingType", "value": "Auction"}]
        response = self.api.execute(
            "findItemsAdvanced",
            {"keywords": query, "sortOrder": sort_order, "itemFilter": itemFilters},
        )

        items = []

        for item in response.reply.searchResult.item:
            items.append(
                {
                    "item_id": f"ebay-{item.itemId}",
                    "name": item.title,
                    "url": item.viewItemURL,
                    "start_time": item.listingInfo.startTime,
                    "end_time": item.listingInfo.endTime,
                    "price": float(item.sellingStatus.convertedCurrentPrice.value),
                    "image_url": item.galleryURL.replace("/thumbs", "").replace(
                        "s-l140", "s-l1600"
                    ),
                }
            )
        return items

    def get_item_details(self, item_id):
        raise NotImplementedError("eBay does not support item details yet")

        response = self.api.execute("findItemsByProduct", {"productId": item_id})
        item = response.reply.searchResult.item
        return item
