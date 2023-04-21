from confluent_kafka import Producer

from src.shared.json import jsonify


class MessageProducer:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix + ("/" if prefix else "")
        self.producer = Producer(
            bootstrap_servers="localhost:29092",
            value_serializer=lambda v: jsonify(v).encode("utf-8"),
        )

    def send(self, topic, data):
        self.producer.send(self.prefix + topic, data)

    def flush(self):
        self.producer.flush()

    def close(self):
        self.producer.close()
