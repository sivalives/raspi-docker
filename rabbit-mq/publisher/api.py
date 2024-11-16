import json
import pika
from flask import Flask, request, jsonify

# RabbitMQ settings
rabbitmq_host = "rabbitmq"
port = 5672

# Flask app initialization
app = Flask(__name__)

# Queue mapping (key: API input, value: queue name)
queue_mapping = {
    "fish": "fish_queue",
    "lifx": "lifx_queue",
    "queue3": "my_queue_3",
}

# Establish connection to RabbitMQ with heartbeat
def create_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=port,
            heartbeat=600  # Heartbeat interval in seconds (10 minutes)
        )
    )
    channel = connection.channel()
    
    # Declare all queues in the mapping
    for queue in queue_mapping.values():
        channel.queue_declare(queue=queue)
    
    return connection, channel

# Create connection and channel initially
connection, channel = create_channel()

@app.route('/publish', methods=['POST'])
def publish():
    """Handle incoming REST API calls to publish data to RabbitMQ."""
    global connection, channel
    
    data = request.get_json()

    if not data or "queue" not in data or "message" not in data:
        return jsonify({"error": "Missing 'queue' or 'message' in request body"}), 400

    queue = queue_mapping.get(data["queue"])
    if not queue:
        return jsonify({"error": f"Queue '{data['queue']}' is not configured"}), 400

    try:
        # Check if channel is closed and re-establish if necessary
        if channel.is_closed:
            print("Channel is closed, reconnecting...")
            connection, channel = create_channel()
        
        # Publish message to the specified queue
        message = json.dumps(data["message"])
        channel.basic_publish(exchange="", routing_key=queue, body=message)

        return jsonify({"status": "success", "message": f"Message published to {queue}!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

