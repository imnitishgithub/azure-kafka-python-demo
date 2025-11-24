import json
from confluent_kafka import Consumer, KafkaException

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
    "group.id": "demo-consumer-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

print("Consumer started... waiting for messages.\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        print(
            f"Received: partition={msg.partition()} "
            f"offset={msg.offset()} "
            f"value={msg.value().decode()}"
        )

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    consumer.close()
