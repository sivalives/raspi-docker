import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Disable warnings
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin numbering
PIN = 18  # Example pin number

GPIO.setup(PIN, GPIO.OUT)  # Set the pin as an output

# Turn the pin on and off
GPIO.output(PIN, GPIO.HIGH)  # Turn the pin on (set to high)
time.sleep(1)  # Wait for 1 second
GPIO.output(PIN, GPIO.LOW)   # Turn the pin off (set to low)

GPIO.cleanup()  # Clean up and reset the GPIO pins

