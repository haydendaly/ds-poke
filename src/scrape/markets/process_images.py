from src.shared.storage import Database, ImageStorage
from src.shared.threading import KafkaWorkerBase


class ListingImageDownloader(KafkaWorkerBase):
    def __init__(self):
        super().__init__(pattern="semiprocessed-listings.*")

        self.yahoo_auctions_storage = ImageStorage("yahoo-auctions", db=Database.LOCAL)
        self.mercari_storage = ImageStorage("mercari", db=Database.LOCAL)

    async def process_message(self, message):
        try:
            market = message["market"]
            print(
                f"Downloading image for {market} listing {message['item_id']}",
                message["images"],
            )
            for i, image_url in enumerate(message["images"]):
                image_id = f"{message['item_id']}_{i}"
                if market == "yahoo-auctions":
                    await self.yahoo_auctions_storage.download_to_id_async(
                        image_url, image_id
                    )
                elif market == "mercari":
                    await self.mercari_storage.download_to_id_async(image_url, image_id)
        except Exception as e:
            print(e)
            return False, e
        return True, None


async def run():
    async with ListingImageDownloader() as listing_image_downloader:
        await listing_image_downloader.run()
