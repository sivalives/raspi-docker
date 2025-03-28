import RPi.GPIO as GPIO
import time
from log2rabbitmq import publish2rmq
from datetime import datetime

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

        if switch_state == GPIO.HIGH:
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)  # Turn motor OFF
        else:
            GPIO.output(OUTPUT_PIN, GPIO.LOW)   # Turn motor ON
            data = {
                    "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    "job_name": "fish-topup-water",
                    "job_status": "success",  # Or "Completed", "Failed", etc.
                    "job_error": None,  # Use error message if the job fails, or None if no error
                    "comments" : "topped up water in tank"
                    }
            rmq_data = {"message":data}
            #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
            publish2rmq(rmq_data)

        time.sleep(0.5)  # Wait 500ms

except KeyboardInterrupt:
    print("Stopping program.")

finally:
    GPIO.cleanup()

