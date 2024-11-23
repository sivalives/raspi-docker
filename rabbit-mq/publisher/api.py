import json
import pika
from flask import Flask, request, jsonify

# RabbitMQ settings
rabbitmq_host = "rabbitmq"
port = 5672
EXCHANGE_NAME = "raspberry_exchange"
ROUTING_KEY = "fish"
credentials = pika.PlainCredentials('admin', 'guest')

# Flask app initialization
app = Flask(__name__)

# Establish connection to RabbitMQ with heartbeat
def create_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=port,
            credentials=credentials,
            heartbeat=600  # Heartbeat interval in seconds (10 minutes)
        )
    )
    channel = connection.channel()
    
    return connection, channel

# Create connection and channel initially
connection, channel = create_channel()

@app.route('/publish', methods=['POST'])
def publish():
    """Handle incoming REST API calls to publish data to RabbitMQ."""
    global connection, channel
    
    data = request.get_json()

    try:
        # Check if channel is closed and re-establish if necessary
        if channel.is_closed:
            print("Channel is closed, reconnecting...")
            connection, channel = create_channel()
        
        # Publish message to the specified queue
        message = json.dumps(data["message"])
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY, body=message)

        return jsonify({"status": "success", "message": f"Message published to {EXCHANGE_NAME}->{ROUTING_KEY}!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

