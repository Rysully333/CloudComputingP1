from kafka import KafkaConsumer
import json
import requests

url = "http://192.168.5.247:5000/predict"

dbConsumer = KafkaConsumer(
    'images',
    group_id='ml-consumer',
    bootstrap_servers=['192.168.5.18:9092'],
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    consumer_timeout_ms=2000,
    enable_auto_commit=True,
    auto_offset_reset='earliest'
)

for message in dbConsumer:
    # Send just the data field of the json message
    requests.post(url, json=message.value.get("data"))