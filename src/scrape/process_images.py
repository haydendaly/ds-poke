from src.scrape.markets import Market, PartialListingDetails
from src.shared.storage import Database, ImageStorage
from src.shared.threading import MessageWorkerBase


class ListingImageDownloader(MessageWorkerBase):
    def __init__(self):
        super().__init__(pattern="semiprocessed-listings.*")

        yahoo_auctions_storage = ImageStorage(
            str(Market.YAHOO_AUCTIONS), db=Database.LOCAL
        )
        mercari_storage = ImageStorage(str(Market.MERCARI), db=Database.LOCAL)
        self.markets = {
            Market.YAHOO_AUCTIONS: yahoo_auctions_storage,
            Market.MERCARI: mercari_storage,
        }

    def validate_message_format(self, message) -> bool:
        return isinstance(message, PartialListingDetails)

    async def process_message(self, message):
        try:
            market = message["market"]
            print(
                f"Downloading image for {market} listing {message['item_id']}",
                message["images"],
            )
            market = message["market"]
            if market not in self.markets:
                return False, f"unknown market {market}"

            for i, image_url in enumerate(message["images"]):
                image_id = f"{message['item_id']}_{i}"
                await self.markets[market].download_to_id_async(image_url, image_id)

        except Exception as e:
            return False, e
        return True, None


async def run():
    async with ListingImageDownloader() as listing_image_downloader:
        await listing_image_downloader.run()
