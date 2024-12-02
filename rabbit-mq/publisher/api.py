import json
import time
import pika
from flask import Flask, request, jsonify

# RabbitMQ settings
rabbitmq_host = "rabbitmq"
port = 5672
EXCHANGE_NAME = "raspberry_exchange"
credentials = pika.PlainCredentials('admin', 'guest')

# Flask app initialization
app = Flask(__name__)

def create_channel():
    """
    Establish a new connection and channel to RabbitMQ.
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=port,
                credentials=credentials,
                heartbeat=60  # Send heartbeat every 60 seconds
            )
        )
        channel = connection.channel()
        print("RabbitMQ connection and channel established.")
        return connection, channel
    except Exception as e:
        print(f"Error creating RabbitMQ connection/channel: {e}")
        raise

# Create connection and channel initially
try:
    connection, channel = create_channel()
except Exception as e:
    print(f"Failed to initialize RabbitMQ: {e}")
    connection, channel = None, None

@app.route('/publish', methods=['POST'])
def publish():
    """Handle incoming REST API calls to publish data to RabbitMQ."""
    global connection, channel

    data = request.get_json()
    retries = int(request.args.get("retries", 3))  # Default to 3 retries if not specified
    ROUTING_KEY = request.args.get("routing_key")

    if not ROUTING_KEY:
        return jsonify({"error": f"Empty routing key cannot publish data to MQ {data}"}), 500

    for attempt in range(retries):
        try:
            # Check if connection is closed or not initialized
            if connection is None or connection.is_closed:
                print("Connection is closed or None, reconnecting...")
                connection, channel = create_channel()

            # Check if channel is closed
            if channel.is_closed:
                print("Channel is closed, reconnecting...")
                connection, channel = create_channel()

            # Publish the message
            message = json.dumps(data["message"])
            channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY, body=message)

            print(f"Message successfully published on attempt {attempt + 1}.")
            return jsonify({"status": "success", "message": f"Message published to {EXCHANGE_NAME}->{ROUTING_KEY}!"}), 200
        except Exception as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff: 1, 2, 4 seconds...
            else:
                # Log final failure
                print(f"Failed to publish message after {retries} attempts.")
                return jsonify({"error": f"Failed to publish after {retries} retries: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

