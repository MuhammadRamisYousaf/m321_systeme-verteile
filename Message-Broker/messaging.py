import argparse
import time
from itertools import count

import pika


CONSUMERS = ("A", "B")
SHARED_QUEUE = "m321.round-robin"
FANOUT_EXCHANGE = "m321.fanout"


def configure(channel, mode):
    if mode == "round-robin":
        channel.queue_declare(queue=SHARED_QUEUE, durable=True)
        return

    channel.exchange_declare(exchange=FANOUT_EXCHANGE, exchange_type="fanout", durable=True)
    for name in CONSUMERS:
        queue = f"{FANOUT_EXCHANGE}.{name}"
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue=queue, exchange=FANOUT_EXCHANGE)


def produce(channel, mode):
    exchange, routing_key = ("", SHARED_QUEUE)
    if mode == "fanout":
        exchange, routing_key = (FANOUT_EXCHANGE, "")

    for number in count(1):
        message = f"Hello World #{number}"
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        print(f"Producer: {message}", flush=True)
        time.sleep(1)


def consume(channel, mode, name):
    queue = SHARED_QUEUE if mode == "round-robin" else f"{FANOUT_EXCHANGE}.{name}"

    def on_message(channel, method, properties, body):
        print(f"Consumer {name}: {body.decode('utf-8')}", flush=True)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=on_message)
    print(f"Consumer {name} wartet auf {queue}", flush=True)
    channel.start_consuming()


def main():
    parser = argparse.ArgumentParser(description="RabbitMQ routing demo")
    parser.add_argument("mode", choices=("round-robin", "fanout"))
    roles = parser.add_subparsers(dest="role", required=True)
    roles.add_parser("producer")
    consumer = roles.add_parser("consumer")
    consumer.add_argument("name", choices=CONSUMERS)
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
    try:
        channel = connection.channel()
        configure(channel, args.mode)
        if args.role == "producer":
            produce(channel, args.mode)
        else:
            consume(channel, args.mode, args.name)
    except KeyboardInterrupt:
        pass
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
