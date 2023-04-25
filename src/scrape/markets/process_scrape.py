import asyncio
import concurrent.futures
import os

from src.scrape.markets import MercariMarket, YahooAuctionsMarket
from src.shared.threading import KafkaWorkerBase


class SegmentationMock:
    def get_card_bounds(self, image_url):
        return [
            {"x": 0, "y": 0, "width": 100, "height": 100},
        ]


class ListingProcessor(KafkaWorkerBase):
    def __init__(self):
        super().__init__(
            pattern="raw-listings.*", num_threads=(os.cpu_count() or 5) * 4
        )

        self.yahoo_auctions = YahooAuctionsMarket()
        self.mercari = MercariMarket()
        self.segmentation = SegmentationMock()
        self.yahoo_auctions_semaphore = asyncio.Semaphore(10)
        self.mercari_semaphore = asyncio.Semaphore(10)

    def validate_message_format(self, message):
        required_keys = {"price", "title", "thumbnail_url", "item_id", "market"}
        return all(key in message for key in required_keys)

    async def process_message(self, message):
        if not self.validate_message_format(message):
            return False, "invalid message format"
        try:
            thumbnail_url = message["thumbnail_url"]
            card_bounds = self.segmentation.get_card_bounds(thumbnail_url)
            if not card_bounds:
                return False, "no card bounds"

            if message["market"] == self.yahoo_auctions.name:
                async with self.yahoo_auctions_semaphore:
                    item_details = self.yahoo_auctions.get_item_details(
                        message["item_id"]
                    )
                    item = {**message, **item_details}
                    print(item)
                    await self.message_producer.send(
                        f"semiprocessed-listings.{self.yahoo_auctions.name}", item
                    )
            elif message["market"] == self.mercari.name:
                async with self.mercari_semaphore:
                    # TODO(hayden): implement get_item_details
                    pass
            else:
                return False, f"unknown market {message['market']}"

        except Exception as e:
            return False, e
        return True, None


async def run():
    async with ListingProcessor() as listing_processor:
        await listing_processor.run()
