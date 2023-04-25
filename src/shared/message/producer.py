from aiokafka import AIOKafkaProducer

from src.shared.json import jsonify


class MessageProducer:
    def __init__(self):
        pass

    async def __aenter__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers="localhost:29092",
            value_serializer=lambda v: jsonify(v).encode("utf-8"),
        )
        await self.producer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def send(self, topic, data):
        await self.producer.send(topic, data)

    async def flush(self):
        await self.producer.flush()

    async def close(self):
        await self.producer.stop()
