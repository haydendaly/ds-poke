import asyncio
import os


class WorkerBase:
    def __init__(self, num_threads=None):
        self.queue = asyncio.Queue()
        self.num_threads = num_threads or os.cpu_count() or 1

    async def worker(self):
        raise NotImplementedError("You must implement the worker method.")

    async def run(self):
        raise NotImplementedError("You must implement the worker method.")
