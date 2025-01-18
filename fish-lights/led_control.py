import pika
import RPi.GPIO as GPIO
import sys
import json

rabbitmq_host = "rabbitmq"  # RabbitMQ hostname or IP address
rabbitmq_port = 5672
rabbitmq_queue = "led_queue"

# Pin configuration
PIN = 6  # GPIO pin connected to the LED
GPIO.setwarnings(False)  # Disable warnings

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(PIN, GPIO.OUT)  # Set the pin as an output

# Flag to control the LED state
led_on = False

def turn_on():
    """Turn on the LED."""
    global led_on
    print("Turning LED on...")
    GPIO.output(PIN, GPIO.HIGH)  # GPIO.HIGH turns the pin on
    led_on = True

def turn_off():
    """Turn off the LED."""
    global led_on
    print("Turning LED off...")
    GPIO.output(PIN, GPIO.LOW)  # GPIO.LOW turns the pin off
    led_on = False

def callback(ch, method, properties, body):
    """Callback to process messages from RabbitMQ."""
    payload = body.decode('utf-8')  # Decode the message body
    payload_json = json.loads(payload)
    print(f"Received payload: {payload_json}")

    light_state = payload_json.get("light_state")

    if light_state == "on":
        turn_on()
    elif light_state == "off":
        turn_off()
    else:
        print(f"Unknown payload: {payload}")

def main():
    """Set up RabbitMQ consumer and listen for messages."""
    try:
        # Connect to RabbitMQ
        credentials = pika.PlainCredentials('admin', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rabbitmq_host, port=rabbitmq_port, credentials=credentials,))
        channel = connection.channel()

        # Declare a queue to listen to
        channel.queue_declare(queue=rabbitmq_queue, durable=True)  # Updated queue name to 'led_queue'

        # Set up the consumer to listen for messages
        channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nExiting program on user interrupt.")
    finally:
        # Cleanup GPIO settings when the program exits
        GPIO.cleanup()
        print("GPIO cleanup done.")

if __name__ == "__main__":
    main()

