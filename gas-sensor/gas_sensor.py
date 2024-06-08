import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)  # Using BCM numbering
gas_sensor_pin = 4  # GPIO pin 4 for gas sensor output
buzzer_pin = 12  # GPIO pin 12 for buzzer output

# Set up the gas sensor pin
GPIO.setup(gas_sensor_pin, GPIO.IN)

try:
    gas_leak_detected = False  # Track the state of gas leak detection

    while True:
        # Read the value from the gas sensor pin
        gas_detected = GPIO.input(gas_sensor_pin)
        print(f"Gas sensor output (GPIO pin 4): {gas_detected}")

        # Gas sensor returns 1 normally; when there is a gas leak it will return 0
        if gas_detected == 0:
            if not gas_leak_detected:
                gas_leak_detected = True
                GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.HIGH)  # Set up and turn the buzzer on
                print("Gas leak detected! Buzzer (GPIO pin 12) set to HIGH")
        else:
            if gas_leak_detected:
                gas_leak_detected = False
                GPIO.output(buzzer_pin, GPIO.LOW)  # Turn the buzzer off
                GPIO.cleanup(buzzer_pin)  # Clean up the buzzer pin
                print("No gas leak. Buzzer (GPIO pin 12) set to LOW and cleaned up")

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Clean up all GPIO settings
    GPIO.cleanup()
    print("Program terminated and all GPIO cleaned up.")

