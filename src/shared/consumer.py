from typing import List

from kafka import KafkaConsumer

from .json import json_loads


class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
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
