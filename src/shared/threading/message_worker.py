import asyncio
import concurrent.futures

from src.shared.message import MessageConsumer, MessageProducer
from src.shared.threading.worker import WorkerBase


class MessageWorkerBase(WorkerBase):
    def __init__(self, pattern, num_threads=None):
        self.pattern = pattern
        super().__init__(num_threads=num_threads)

    async def __aenter__(self):
        self.message_consumer = await MessageConsumer().__aenter__()
        self.message_producer = await MessageProducer().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.message_consumer.__aexit__(exc_type, exc_val, exc_tb)
        await self.message_producer.__aexit__(exc_type, exc_val, exc_tb)

    async def handle_error(self, error):
        print(error)

    async def worker(self):
        while True:
            message = await self.queue.get()
            success, error = await self.process_message(message)
            if error:
                await self.handle_error(error)
            self.queue.task_done()

    async def run(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_threads
        ) as executor:
            workers = [
                asyncio.create_task(self.worker()) for _ in range(self.num_threads)
            ]
            async for message in self.message_consumer.consume_pattern(self.pattern):
                await self.queue.put(message)
            await self.queue.join()
            for w in workers:
                w.cancel()

    async def process_message(self, message):
        raise NotImplementedError("You must implement the worker method.")
