import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the gas sensor
gas_sensor_pin = 4  # GPIO pin 4 for gas sensor output

# Set up the gas sensor pin
GPIO.setup(gas_sensor_pin, GPIO.IN)

try:
    while True:
        # Read the value from the gas sensor pin
        gas_detected = GPIO.input(gas_sensor_pin)
        
        # Gas sensor returns 1 normally; when there is a gas leak it will return 0
        if gas_detected == 0:
            print("Gas leak detected!")
        
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Clean up all GPIO settings
    GPIO.cleanup()
    print("Program terminated and all GPIO cleaned up.")

