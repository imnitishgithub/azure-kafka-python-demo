#!/bin/bash
set -e

RG="kafka-demo-rg"
LOC="eastus"
NS="kafka-eh-$(openssl rand -hex 3)"
EH="demo-topic"

echo "Creating resource group..."
az group create -n $RG -l $LOC

echo "Creating Event Hubs namespace..."
az eventhubs namespace create \
  --name $NS \
  --resource-group $RG \
  --location $LOC \
  --sku Standard

echo "Creating Event Hub (topic)..."
az eventhubs eventhub create \
  --name $EH \
  --namespace-name $NS \
  --resource-group $RG \
  --partition-count 4

echo "Getting connection string..."
CONN=$(az eventhubs namespace authorization-rule keys list \
  --namespace-name $NS \
  --resource-group $RG \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv)

echo "--------------------------------------------"
echo "Namespace: $NS"
echo "Event Hub: $EH"
echo "Connection String:"
echo "$CONN"
echo "--------------------------------------------"

echo "Add these values to eventhubs_kafka/config.json"
