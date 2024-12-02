import requests
import json

#pass routing key as query parameter
url = "http://rabbitmq-publisher:5000/publish?routing_key=fish"

def publish2rmq(data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data successfully published!")
        return True
    else:
        print("Failed to publish data:", response.json())
        return False
