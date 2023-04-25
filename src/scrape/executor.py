import asyncio
import time

from src.scrape.markets import Market, MercariMarket, YahooAuctionsMarket
from src.shared.cache import Cache, CacheDatabase
from src.shared.message import MessageProducer


class MarketExecutor:
    def __init__(self, min_interval=10, max_interval=300):
        yahoo_auctions = YahooAuctionsMarket()
        mercari = MercariMarket()
        self.markets = {
            yahoo_auctions.name: yahoo_auctions,
            mercari.name: mercari,
        }
        self.cache = Cache(CacheDatabase.AUCTION)
        self.min_interval = min_interval
        self.max_interval = max_interval

    async def __aenter__(self):
        self.message_producer = await MessageProducer().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.message_producer.__aexit__(exc_type, exc_val, exc_tb)

    # adapt query interval based on speed
    def calculate_interval(self, speed):
        interval_range = self.max_interval - self.min_interval
        adaptive_interval = interval_range * (1 - speed) + self.min_interval
        return min(max(adaptive_interval, self.min_interval), self.max_interval)

    async def execute_market(self, market: Market, query):
        while True:
            start_time = time.time()
            items = self.markets[market].search(query)

            if items:
                new_items = 0
                total_items = len(items)

                for item in items:
                    item_id = item["item_id"]
                    exists = self.cache.exists(item_id)

                    if not exists:
                        self.cache.set(item_id, item)
                        await self.message_producer.send(f"raw-listings.{market}", item)
                        new_items += 1

                speed = new_items / total_items
                interval = self.calculate_interval(speed)
                execution_time = time.time() - start_time
                print(
                    f"Market: {market}, New Items: {new_items}, Total Items: {total_items}, Speed: {speed}, Interval: {interval}, Execution Time: {execution_time}"
                )

            else:
                interval = self.max_interval

            await asyncio.sleep(interval)

    async def run(self, query):
        tasks = []
        for market in self.markets.values():
            task = asyncio.create_task(self.execute_market(market, query))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def run():
    async with MarketExecutor() as executor:
        await executor.run("pokemon")
