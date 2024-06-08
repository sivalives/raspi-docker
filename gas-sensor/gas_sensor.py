import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)  # Using BCM numbering
gas_sensor_pin = 4  # GPIO pin 4 for gas sensor output
buzzer_pin = 12  # GPIO pin 12 for buzzer input

# Set up the GPIO pins
GPIO.setup(gas_sensor_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.HIGH)  # Ensure the buzzer starts in the off state

try:
    while True:
        # Read the value from the gas sensor pin
        gas_detected = GPIO.input(gas_sensor_pin)
        print(f"Gas sensor output (GPIO pin 4): {gas_detected}")

        # Gas sensor returns 1 all the time, when there is a gas leak it will return 0
        if gas_detected == 0:
            GPIO.output(buzzer_pin, GPIO.LOW)
            print("Buzzer (GPIO pin 12) set to LOW")
        else:
            GPIO.output(buzzer_pin, GPIO.HIGH)
            print("Buzzer (GPIO pin 12) set to HIGH")

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Clean up the GPIO settings
    GPIO.cleanup()
    print("Program terminated.")

