# Code to run specific parts of robot, expected to change depending on what is needed
# Ignore this as this is a module for the raspberry pi
import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor 1 Code

# Define GPIO pins
DIR_1 = 23     # Direction GPIO pin
STEP_1 = 18    # Step GPIO pin
ENABLE_1 = 24  # Enable GPIO pin (can also be connected to GND if not used)

# Set up GPIO pins as output
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)
GPIO.setup(ENABLE_1, GPIO.OUT)

# Set ENABLE to LOW to enable the motor
GPIO.output(ENABLE_1, GPIO.LOW)

# Set motor direction (Clockwise or Counter-Clockwise)
GPIO.output(DIR_1, GPIO.HIGH)  # Change to GPIO.LOW for counter-clockwise

# Define step delay and step count
step_count = 200        # Number of steps for a full rotation (1.8° per step for most motors)
delay = 0.002           # Delay between steps (controls speed)

# Step the motor
print("Starting the motor...")
for _ in range(step_count):
    GPIO.output(STEP_1, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(STEP_1, GPIO.LOW)
    time.sleep(delay)

# Clean up GPIO pins
GPIO.cleanup()

# Motor 2 Code

# Motor 3 Code

# Servo Motor Calling after it is done
