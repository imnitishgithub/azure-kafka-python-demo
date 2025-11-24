# Azure Kafka (Event Hubs) Python Demo  
This repository contains a complete runnable demo for:

1. **Connecting to Azure Event Hubs using the Kafka protocol**
2. **Producing messages to Kafka**
3. **Consuming messages from Kafka**

The demo uses:
- **Python (`confluent-kafka`)**
- **Azure Event Hubs (Kafka endpoint)**
- **Azure CLI for resource creation (optional)**


## Below is the full repo structure, followed by the content of each file.

azure-kafka-python-demo/
├── README.md
├── .gitignore
├── requirements.txt
├── eventhubs_kafka/
└── scripts/
  
eventhubs_kafka/
  ├── producer.py
  ├── consumer.py
  └── config_sample.json

scripts/
    └── create_eventhubs.sh
    
---


# Quick Start

## 1. Clone the repo

git clone https://github.com/<your-user>/azure-kafka-python-demo.git
cd azure-kafka-python-demo

## 2. Install dependencies

**Ensure librdkafka is installed:**

sudo apt update && sudo apt install -y librdkafka-dev build-essential python3-dev

**Then install Python packages:**

pip install -r requirements.txt


## 3. Create Azure Event Hubs (Kafka Endpoint)

./scripts/create_eventhubs.sh

This script creates:

   Resource group
   Event Hubs namespace
   Event Hub named demo-topic
   Outputs connection strings


## 4. Configure the App

Copy the sample configuration file:

cp eventhubs_kafka/config_sample.json eventhubs_kafka/config.json

Edit config.json:

{
    "EH_NAMESPACE": "demo-kafka-eh-12345",
    "CONNECTION_STRING": "Endpoint=sb://....",
    "TOPIC": "demo-topic"
}


## 5. Run Producer

python eventhubs_kafka/producer.py

You should see:

Delivered to demo-topic [0] at offset 0
...
Done producing


## 6. Run Consumer

python eventhubs_kafka/consumer.py

Expected output:

Received: partition=0 offset=0 value=message-1
...






