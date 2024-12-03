from machine import Pin, PWM
import time

# Initialize servo pin
servo_pin = 2  # GPIO pin for the pen servo
servo = PWM(Pin(servo_pin))
servo.freq(50)  # Set servo PWM frequency to 50Hz

# Function to test servo movement
def test_servo():
    print("Moving to 0°")
    servo.duty_u16(2300)  # Adjust this value if necessary for your servo
    time.sleep(1)

    print("Moving to 90°")
    servo.duty_u16(5000)  # Adjust this value as needed
    time.sleep(1)

    print("Moving to 180°")
    servo.duty_u16(7500)  # Adjust this value as needed
    time.sleep(1)

    # Reset to initial state
    print("Resetting to 0°")
    servo.duty_u16(2300)
    time.sleep(1)

# Run the test
test_servo()
