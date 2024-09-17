import base64
import json
# from kafka import KafkaProducer
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