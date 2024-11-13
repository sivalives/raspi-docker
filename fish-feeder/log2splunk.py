import requests
import json
from datetime import datetime

# Define the Splunk KV Store details
SPLUNK_HOST = "https://10.0.0.13:8089"
SPLUNK_TOKEN = "eyJraWQiOiJzcGx1bmsuc2VjcmV0IiwiYWxnIjoiSFM1MTIiLCJ2ZXIiOiJ2MiIsInR0eXAiOiJzdGF0aWMifQ.eyJpc3MiOiJhZG1pbiBmcm9tIDA5NjdmZmYzNzJlZSIsInN1YiI6ImFkbWluIiwiYXVkIjoicmFzcGkiLCJpZHAiOiJTcGx1bmsiLCJqdGkiOiI1ZTU0NzM0YjVhNDAyYThjMjdjN2FkOWNmNGVhMmQ0MmVhNzg3YmNlOGRiNTdhMDMwOGNlNjgzODc0OGVjNzAzIiwiaWF0IjoxNzMxNTEyODI0LCJleHAiOjE3OTQ1OTQ1NDAsIm5iciI6MTczMTUxMjg4NH0.xyG9_rcl1Ul8swng2acaU6P0RXmKSvUKuMnvCSEDoI0pxyX4p6A4p-4NGyWI5X7XG7vyMvwRigUxLQgsFTBmQg"
APP_NAME = "splunk-raspi-connect"
COLLECTION_NAME = "raspi_collection"

def log2splunk(data):
    """
    Logs data to a Splunk KV Store collection. Creates a new record if no `_key` is provided;
    updates the record if `_key` is present in `data`.
    
    :param data: A dictionary containing the data to log. If `_key` is in the dictionary, 
                 it updates the record; otherwise, it creates a new record.
    :return: The response from the Splunk server.
    """
    headers = {
        "Authorization": f"Bearer {SPLUNK_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Check if the dictionary contains `_key` for an update
    if "_key" in data:
        # Update the existing record using the `_key`
        url = f"{SPLUNK_HOST}/servicesNS/nobody/{APP_NAME}/storage/collections/data/{COLLECTION_NAME}/{data['_key']}"
        response = requests.put(url, headers=headers, data=json.dumps(data),verify=False)
    else:
        # Create a new record
        url = f"{SPLUNK_HOST}/servicesNS/nobody/{APP_NAME}/storage/collections/data/{COLLECTION_NAME}"
        response = requests.post(url, headers=headers, data=json.dumps(data),verify=False)
    
    # Check for success and print the response
    if response.status_code in (200, 201):
        print("Success:", response.json())
    else:
        print("Failed:", response.status_code, response.text)

    return response

# Example usage
'''
if __name__ == "__main__":
    # Example data dictionary to add or update in Splunk KV Store
    # Example data dictionary to add or update in Splunk KV Store
    example_data = {
        "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "job_name": "Job123",
        "job_status": "Running",  # Or "Completed", "Failed", etc.
        "job_error": None,  # Use error message if the job fails, or None if no error
    } 
    log2splunk(example_data)
'''
