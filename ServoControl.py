import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the servo
SERVO_PIN = 18  # Change this to the GPIO pin you are using

# Set up the GPIO pin as an output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM on the servo pin with a frequency of 50Hz (20ms period)
pwm = GPIO.PWM(SERVO_PIN, 50)

# Start PWM with a duty cycle of 0 (off)
pwm.start(0)


def set_servo_angle(angle):
    """
    Set the servo motor to a specific angle.
    :param angle: The angle to set the servo to (0 to 180 degrees).
    """
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # Calculate the duty cycle based on the angle
    duty_cycle = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Give the servo time to move


def cleanup():
    """
    Clean up the GPIO settings and stop the PWM.
    """
    pwm.stop()
    GPIO.cleanup()


# Example usage
if __name__ == "__main__":
    try:
        while True:
            # Move the servo to 0 degrees
            set_servo_angle(0)
            time.sleep(1)

            # Move the servo to 90 degrees
            set_servo_angle(90)
            time.sleep(1)

            # Move the servo to 180 degrees
            set_servo_angle(180)
            time.sleep(1)

    except KeyboardInterrupt:
        cleanup()