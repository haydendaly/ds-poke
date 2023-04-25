import asyncio
from typing import Optional, Tuple

from src.scrape.markets import (Listing, Market, MercariMarket, PartialListing,
                                PartialListingDetails, YahooAuctionsMarket)
from src.shared.threading import MessageWorkerBase


class SegmentationMock:
    def get_card_bounds(self, image_url):
        return [
            {"x": 0, "y": 0, "width": 100, "height": 100},
        ]


class ListingProcessor(MessageWorkerBase):
    MAX_CONNECTIONS_PER_MARKET = 10

    def __init__(self):
        super().__init__(pattern="raw-listings.*")

        yahoo_auctions = YahooAuctionsMarket()
        yahoo_auctions_semaphore = asyncio.Semaphore(self.MAX_CONNECTIONS_PER_MARKET)

        mercari = MercariMarket()
        # TODO(hayden): figure out how to support parallelism for CSR
        mercari_semaphore = asyncio.Semaphore(1)

        self.markets = {
            yahoo_auctions.name: {
                "market": yahoo_auctions,
                "semaphore": yahoo_auctions_semaphore,
            },
            mercari.name: {"market": mercari, "semaphore": mercari_semaphore},
        }
        self.segmentation = SegmentationMock()

    async def process_message(
        self, message: PartialListing
    ) -> Tuple[bool, Optional[str]]:
        try:
            thumbnail_url = message["thumbnail_url"]
            card_bounds = self.segmentation.get_card_bounds(thumbnail_url)
            if not card_bounds:
                return False, "no card bounds"

            market = Market(message["market"])
            if market not in self.markets:
                return False, f"unsupported market {market}"
            topic = f"semiprocessed-listings.{market.value}"

            async with self.markets[market]["semaphore"]:
                item_details: PartialListingDetails = self.markets[market][
                    "market"
                ].get_item_details(message["item_id"])

                item: Listing = {**message, **item_details}  # type: ignore
                await self.message_producer.send(topic, item)

        except Exception as e:
            return False, str(e)
        return True, None


async def run():
    async with ListingProcessor() as listing_processor:
        await listing_processor.run()
