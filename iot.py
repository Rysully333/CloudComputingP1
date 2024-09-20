import base64
import json
import time # for sleep
from kafka import KafkaProducer  # producer of events
from kafka.vendor.six.moves import range
from PIL import Image, ImageFilter
from torchvision import datasets, transforms
import io
import random
import uuid

# Load CIFAR-10 dataset
dataset = datasets.CIFAR10(root='./data', download=True, transform=transforms.ToTensor())

def emulate_camera_feed():
    # randomly select img and correct label from dataset
    img, label = random.choice(dataset)

    # add blurriness/noise by converting img to PIL and add blur
    img_pil = transforms.ToPILImage()(img).filter(ImageFilter.GaussianBlur(radius=2))

    # convert img to bytes for transmission
    buffered = io.BytesIO()
    img_pil.save(buffered, format='JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    ID = str(uuid.uuid4())
    groundtruth = dataset.classes[label]
    
    # create JSON object
    data = {
        "ID": ID,
        "GroundTruth": groundtruth,
        "Data": img_str
    }

    # return JSON obj
    return data

result = emulate_camera_feed()
print(result)

# encode JSON to bytes
def serialize_json(value):
    json_string = json.dumps(value)
    json_bytes = json_string.encode('utf-8')
    return json_bytes

# acquire the producer
producer = KafkaProducer(
    bootstrap_servers="192.168.5.18:9092", 
    acks=1,
    value_serializer=serialize_json  # serialize JSON to bytes
)

# send the contents 100 times after a sleep of 1 sec in between
for i in range(100):
    
    # generate the data
    data = emulate_camera_feed()
    print(data)

    # send the data under topic images
    producer.send("images", value=data)
    producer.flush()

    # sleep a second
    time.sleep(1)

producer.close()