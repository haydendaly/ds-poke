from typing import List

from kafka import KafkaConsumer

from src.shared.json import json_loads


class MessageConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=["localhost:29092"],
            value_deserializer=lambda v: json_loads(v),
        )

    def consume_topics(self, topics: List[str]):
        self.consumer.subscribe(topics)
        for message in self.consumer:
            yield message.value

    def consume_pattern(self, pattern: str = "*"):
        self.consumer.subscribe(pattern=pattern)
        for message in self.consumer:
            yield message.value

    def close(self):
        self.consumer.close()
