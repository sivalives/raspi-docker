import requests
import json

url = "http://localhost:5000/publish"
data = {
    "temperature": 22.5,
    "humidity": 60,
    "status": "OK"
}
#message_type maps to a topic in api.py
mqqt_data = {
    "message_type": "fish_data",
    "message": data }

response = requests.post(url, json=mqqt_data)

if response.status_code == 200:
    print("Data successfully published!")
else:
    print("Failed to publish data:", response.json())

