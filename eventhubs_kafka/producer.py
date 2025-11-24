from confluent_kafka import Producer
import time
import json

# ================================
# Azure Event Hubs Kafka Settings
# ================================
bootstrap_servers = "kafka-eh-80f3d7.servicebus.windows.net:9093"

security_config = {
    "bootstrap.servers": bootstrap_servers,
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "$ConnectionString",
    "sasl.password": "Endpoint=sb://kafka-eh-80f3d7.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<YOUR-KEY-HERE>",
}

topic_name = "demo-topic"

# Delivery callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def run_producer():
    print("Connecting to Azure Event Hubs Kafka...")

    producer = Producer(security_config)

    print("Producing 10 messages...")

    for i in range(10):
        data = {"message": f"Hello from Azure Kafka {i}", "id": i}

        producer.produce(
            topic_name,
            json.dumps(data).encode("utf-8"),
            callback=delivery_report
        )

        producer.poll(0)
        time.sleep(0.5)

    producer.flush()
    print("Done.")

if __name__ == "__main__":
    run_producer()
