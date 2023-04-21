from typing import List

from confluent_kafka import Consumer

from src.shared.json import json_loads


class MessageConsumer:
    def __init__(self):
        self.consumer = Consumer(
            bootstrap_servers="localhost:29092",
            value_deserializer=lambda v: json_loads(v),
        )

    def consume_topic(self, topics: List[str]):
        self.consumer.subscribe(topics)
        for message in self.consumer:
            yield message.value

    def consume_all(self):
        for message in self.consumer:
            yield message.value

    def close(self):
        self.consumer.close()
