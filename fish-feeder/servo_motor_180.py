import RPi.GPIO as GPIO
import time
from datetime import datetime
import pytz
from log2rabbitmq import publish2rmq

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the servo
servo_pin = 18  # Using BCM pin numbering

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz PWM frequency

# Initialize the PWM signal
pwm.start(0)

# Function to set the servo angle
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(0)

try:
    # Rotate to 180 degrees and back to 0 degrees two times
    for _ in range(2):
        set_servo_angle(180)
        time.sleep(0.3)
        set_servo_angle(0)
        time.sleep(0.3)
        
    # Print the current IST time once at the end of the loop
    ist_now = datetime.now(pytz.timezone('Asia/Kolkata'))
    print("Loop completed at:", ist_now.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    data = {
        "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "job_name": "fish-feeder",
        "job_status": "success",  # Or "Completed", "Failed", etc.
        "job_error": None,  # Use error message if the job fails, or None if no error
    }
    rmq_data = {"message":data}
    #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
    publish2rmq(rmq_data)
    
finally:
    # Clean up the GPIO settings
    pwm.stop()
    GPIO.cleanup()

