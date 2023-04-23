import time
from threading import Thread

from src.scrape.markets.mercari import MercariMarket
from src.scrape.markets.yahoo_auctions import YahooAuctionsMarket
from src.shared.cache import Cache, CacheDatabase
from src.shared.message import MessageProducer


class MarketExecutor:
    def __init__(self, min_interval=10, max_interval=300, update_speed=0.01):
        self.markets = [MercariMarket(), YahooAuctionsMarket()]
        self.cache = Cache(CacheDatabase.AUCTION)
        self.message_producer = MessageProducer()
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.update_speed = update_speed

    def run(self, query):
        for market in self.markets:
            Thread(target=self.execute_market, args=(market, query)).start()

    def execute_market(self, market, query):
        while True:
            start_time = time.time()
            items = market.search(query)

            if items:
                new_items = 0
                total_items = len(items)

                for item in items:
                    item_id = item["item_id"]
                    exists = self.cache.exists(item_id)

                    if not exists:
                        self.cache.set(item_id, item)
                        self.message_producer.send("listings." + market.name, item)
                        new_items += 1

                speed = new_items / total_items
                interval = self.calculate_interval(speed)
                execution_time = time.time() - start_time
                print(
                    f"Market: {market.name}, New Items: {new_items}, Total Items: {total_items}, Speed: {speed}, Interval: {interval}, Execution Time: {execution_time}"
                )

            else:
                interval = self.max_interval

            time.sleep(interval)

    def calculate_interval(self, speed):
        interval_range = self.max_interval - self.min_interval
        adaptive_interval = interval_range * (1 - speed) + self.min_interval
        return min(max(adaptive_interval, self.min_interval), self.max_interval)


def main():
    executor = MarketExecutor()
    print(executor.run("pokemon"))
