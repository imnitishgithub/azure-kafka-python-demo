import json
import os
from azure.eventhub import EventHubConsumerClient

# Load config.json
with open("config.json") as f:
    config = json.load(f)

EH_NAMESPACE = config["EH_NAMESPACE"]
CONNECTION_STRING = config["CONNECTION_STRING"]
TOPIC = config["TOPIC"]

EVENTHUB_FQDN = f"{EH_NAMESPACE}.servicebus.windows.net"

consumer = EventHubConsumerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    consumer_group="$Default",
    eventhub_name=TOPIC
)

def on_event(partition_context, event):
    print(f"Received Event from partition {partition_context.partition_id}: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

print(f"Listening on Event Hub topic: {TOPIC}")

with consumer:
    consumer.receive(
        on_event=on_event,
        starting_position="-1"   # read from earliest
    )
