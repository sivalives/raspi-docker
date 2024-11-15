import requests
import json

url = "http://mqqt-publisher:5000/publish"

def publish2mqqt(data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data successfully published!")
        return True
    else:
        print("Failed to publish data:", response.json())
        return False
