import asyncio

import src.scrape.process_listings as process_listings


def main():
    asyncio.run(process_listings.run())
