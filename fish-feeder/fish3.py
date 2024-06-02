#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 19
in2 = 12
in3 = 16
in4 = 21

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.0035

step_count_180 = 2048  # 180 degrees (4096 steps is 360°)

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# initializing
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

motor_pins = [in1, in2, in3, in4]
motor_step_counter = 0

def cleanup():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.cleanup()

def rotate_motor(direction, steps):
    global motor_step_counter
    for _ in range(steps):
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        if direction == True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction == False:
            motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

# the meat
try:
    # Rotate 180 degrees clockwise
    rotate_motor(False, step_count_180)
    #time.sleep(1)  # Pause for a second
    # Rotate 180 degrees counter-clockwise
    rotate_motor(True, step_count_180)
except KeyboardInterrupt:
    cleanup()
    exit(1)

cleanup()
exit(0)

