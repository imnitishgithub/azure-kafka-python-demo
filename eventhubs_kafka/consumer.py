from confluent_kafka import Consumer, KafkaException
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
    "group.id": "demo-consumer-group",
    "auto.offset.reset": "earliest",
}

topic_name = "demo-topic"

def run_consumer():
    print("Starting Kafka consumer...")

    consumer = Consumer(security_config)
    consumer.subscribe([topic_name])

    try:
        print("Listening for messages...")
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            message = msg.value().decode("utf-8")
            print(f"Received: {message}")

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()

if __name__ == "__main__":
    run_consumer()
