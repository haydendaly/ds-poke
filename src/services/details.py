import asyncio

import src.scrape.process_listings as process_listings


def process_scrape():
    asyncio.run(process_listings.run())
