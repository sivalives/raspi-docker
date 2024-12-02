import requests
import json

#add the query parameter specific for telegram
url = "http://rabbitmq-publisher:5000/publish?routing_key=telegram"

def publish2rmq(data):
    rmq_data = {"message": data}
    response = requests.post(url, json=rmq_data)
    if response.status_code == 200:
        print("Data successfully published!")
        return True
    else:
        print("Failed to publish data:", response.json())
        return False
