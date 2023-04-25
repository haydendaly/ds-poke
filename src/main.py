import asyncio

import src.scrape.download_listing_images as download_listing_images
import src.scrape.market_executor as market_executor
import src.scrape.process_listings as process_listings


def market():
    asyncio.run(market_executor.run())


def process_scrape():
    asyncio.run(process_listings.run())


def process_images():
    asyncio.run(download_listing_images.run())
