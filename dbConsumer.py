from kafka import KafkaConsumer
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ryanhsullivan:tGWVn60E5ylc1btz@imagesdb.ecwkq.mongodb.net/?retryWrites=true&w=majority&appName=ImagesDB"
# Create a new client and connect to the server
client = MongoClient(uri)

database = client['imagesdb']
collection = database['images']

dbConsumer = KafkaConsumer(
    'images',
    group_id='db-consumer',
    bootstrap_servers=['192.168.5.18:9092'],
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    consumer_timeout_ms=2000,
    enable_auto_commit=True,
    auto_offset_reset='earliest'
)

for message in dbConsumer:
    collection.insert_one({message.value})