import asyncio

import src.scrape.market_executor as market_executor


def market():
    asyncio.run(market_executor.run())
