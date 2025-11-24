import json
import os
import time
from azure.eventhub import EventHubProducerClient, EventData

# Load config.json
with open("config.json") as f:
    config = json.load(f)

EH_NAMESPACE = config["EH_NAMESPACE"]
CONNECTION_STRING = config["CONNECTION_STRING"]
TOPIC = config["TOPIC"]

# Build FQ endpoint for Kafka+EH
EVENTHUB_FQDN = f"{EH_NAMESPACE}.servicebus.windows.net"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    eventhub_name=TOPIC
)

def send_messages():
    print(f"Producing messages to Azure Event Hub Kafka topic: {TOPIC}")
    for i in range(20):
        message = f"Hello message {i}"
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(message))
        producer.send_batch(event_data_batch)
        print(f"Sent: {message}")
        time.sleep(1)

if __name__ == "__main__":
    send_messages()
