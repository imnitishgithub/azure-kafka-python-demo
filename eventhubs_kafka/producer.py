import json
from confluent_kafka import Producer

# Load config
with open("eventhubs_kafka/config.json") as f:
    cfg = json.load(f)

EH_NAMESPACE = cfg["EH_NAMESPACE"]
BOOTSTRAP_SERVER = f"{EH_NAMESPACE}.servicebus.windows.net:9093"
SASL_USERNAME = "$ConnectionString"
SASL_PASSWORD = cfg["CONNECTION_STRING"]
TOPIC = cfg["TOPIC"]

conf = {
    "bootstrap.servers": BOOTSTRAP_SERVER,
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": SASL_USERNAME,
    "sasl.password": SASL_PASSWORD,
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

print("Producing 10 messages...")

for i in range(1, 11):
    value = f"message-{i}"
    producer.produce(TOPIC, value.encode(), callback=delivery_report)
    producer.poll(0)

producer.flush()
print("Done.")
