import asyncio

import src.scrape.executor as executor
import src.scrape.process_images as processor_images
import src.scrape.process_scrape as processor_scrape


def market():
    asyncio.run(executor.run())


def process_scrape():
    asyncio.run(processor_scrape.run())


def process_images():
    asyncio.run(processor_images.run())
