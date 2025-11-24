import os
import json
from confluent_kafka import Producer

# Load config.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

with open(CONFIG_PATH) as f:
    config = json.load(f)

bootstrap_servers = config["bootstrap_servers"]
sasl_username = config["sasl_username"]
sasl_password = config["sasl_password"]
topic_name = config["topic_name"]

kafka_config = {
    "bootstrap.servers": bootstrap_servers,
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": sasl_username,
    "sasl.password": sasl_password
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
    if err:
        print("Delivery failed:", err)
    else:
        print(f"Delivered message to {msg.topic()} [{msg.partition()}]")

print("Producing 10 Kafka messages...")

for i in range(10):
    producer.produce(
        topic_name,
        key=str(i),
        value=f"Message {i} from Kafka Python producer",
        callback=delivery_report
    )
    producer.poll(0)

producer.flush()
print("Done.")
