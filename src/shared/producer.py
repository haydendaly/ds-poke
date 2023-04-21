from kafka import KafkaProducer

from .json import jsonify


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="localhost:29092",
            value_serializer=lambda v: jsonify(v).encode("utf-8"),
        )

    def send(self, topic, data):
        self.producer.send(topic, data)

    def flush(self):
        self.producer.flush()

    def close(self):
        self.producer.close()
