from src.shared.message.consumer import MessageConsumer


def main():
    consumer = MessageConsumer()
    for message in consumer.consume_pattern("listings.*"):
        print(message)
