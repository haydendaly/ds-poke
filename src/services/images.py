import asyncio

import src.scrape.download_listing_images as download_listing_images


def process_images():
    asyncio.run(download_listing_images.run())
