import json
import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify

# MQTT broker settings
broker = "mosquitto"
port = 1883

# Define the MQTT client
client = mqtt.Client()

# Initialize Flask app
app = Flask(__name__)

# Connect to the broker
client.connect(broker, port)
client.loop_start()

# Define a dictionary mapping message types to topics
topic_mapping = {
    "fish_data": "fish/topic",
    "iptv_data": "iptv/topic",
    "lifx_data": "lifx/topic"
}

@app.route('/publish', methods=['POST'])
def publish():
    """Handle incoming REST API calls to publish data to MQTT based on message type."""
    # Get JSON data from POST request
    data = request.get_json()

    if not data or "message" not in data or "message_type" not in data:
        return jsonify({"error": "Invalid JSON data. 'message' and 'message_type' are required."}), 400

    message = data["message"]
    message_type = data["message_type"]

    # Determine the topic based on the message type
    topic = topic_mapping.get(message_type)
    if not topic:
        return jsonify({"error": f"Unknown message type '{message_type}'"}), 400

    try:
        # Convert message to JSON and publish to the determined topic
        payload = json.dumps(message)
        # Publish with retain=True to make the message persistent in the broker, use subscriber to send empty message to clear
        client.publish(topic, payload,retain=True)
        return jsonify({"status": "success", "message": f"Data published successfully to topic '{topic}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Listen on all interfaces for Docker container

