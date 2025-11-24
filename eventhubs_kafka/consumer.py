import os
import json
from confluent_kafka import Consumer

# Load config.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

with open(CONFIG_PATH) as f:
    config = json.load(f)

bootstrap_servers = config["bootstrap_servers"]
sasl_username = config["sasl_username"]
sasl_password = config["sasl_password"]
topic_name = config["topic_name"]
consumer_group = config["consumer_group"]

kafka_config = {
    "bootstrap.servers": bootstrap_servers,
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": sasl_username,
    "sasl.password": sasl_password,
    "group.id": consumer_group,
    "auto.offset.reset": "earliest",
}

consumer = Consumer(kafka_config)
consumer.subscribe([topic_name])

print(f"Listening on topic '{topic_name}' ... Press CTRL+C to stop.\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue

        print(f"Received: {msg.value().decode()} (key={msg.key()})")

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()
