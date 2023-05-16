import asyncio

import src.scrape.market_executor as market_executor


def main():
    asyncio.run(market_executor.run())
