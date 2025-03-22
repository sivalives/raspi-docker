import RPi.GPIO as GPIO
import time

# Define GPIO pins
FLOAT_SWITCH_PIN = 4  # Float switch input
OUTPUT_PIN = 22       # Motor control output

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOAT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use pull-down resistor
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

try:
    while True:
        switch_state = GPIO.input(FLOAT_SWITCH_PIN)  # Read float switch
        motor_state = GPIO.input(OUTPUT_PIN)  # Read motor state

        # Debug output (Reversed)
        print(f"Float Switch: {'HIGH (Water Full)' if switch_state else 'LOW (Water Low)'}, "
              f"Motor: {'OFF' if motor_state else 'ON'}")

        # Reverse logic: Turn ON motor when water is low
        if switch_state == GPIO.HIGH:
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)  # Turn motor ON
        else:
            GPIO.output(OUTPUT_PIN, GPIO.LOW)   # Turn motor OFF

        time.sleep(0.5)  # Wait 500ms

except KeyboardInterrupt:
    print("Stopping program.")

finally:
    GPIO.cleanup()

