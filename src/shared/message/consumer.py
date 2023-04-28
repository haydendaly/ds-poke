from typing import List

from aiokafka import AIOKafkaConsumer

from src.shared.json import json_loads


class MessageConsumer:
    def __init__(self, group_id: str = "default"):
        self.group_id = group_id

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            group_id=self.group_id,
            bootstrap_servers="localhost:29092",
            value_deserializer=lambda v: json_loads(v),
        )
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def commit(self):
        await self.consumer.commit()

    async def consume_topics(self, topics: List[str]):
        self.consumer.subscribe(topics)
        async for message in self.consumer:
            yield message.value
            await self.commit()

    async def consume_pattern(self, pattern: str = "*"):
        self.consumer.subscribe(pattern=pattern)
        async for message in self.consumer:
            yield message.value
            await self.commit()

    async def close(self):
        await self.consumer.stop()
