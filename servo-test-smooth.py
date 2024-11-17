from machine import Pin, PWM
import time

# Set up each servo
shoulder_servo = PWM(Pin(15))  # Shoulder servo on pin 15
elbow_servo = PWM(Pin(16))     # Elbow servo on pin 16
pen_servo = PWM(Pin(17))       # Pen servo on pin 17

# Set frequency
shoulder_servo.freq(50)
elbow_servo.freq(50)
pen_servo.freq(50)

# Helper function to map angle (0-180 degrees) to duty cycle (0-65535)
def angle_to_duty(angle):
    return int(3276 + (angle * 13107 / 180))  # Maps 0-180° 

# Smoothly transition the servo to the target angle
def smooth_move(servo, start_angle, end_angle, step_delay=0.02):
    start_duty = angle_to_duty(start_angle)
    end_duty = angle_to_duty(end_angle)

    # Determine direction of motion
    step = 100 if start_duty < end_duty else -100

    # Gradually move the servo
    for duty in range(start_duty, end_duty, step):
        servo.duty_u16(duty)
        time.sleep(step_delay)

    # Ensure final position is reached
    servo.duty_u16(end_duty)

# Example: Smoothly move each servo
smooth_move(shoulder_servo, 0, 90)   # Move shoulder from 0° to 90°
smooth_move(elbow_servo, 90, 180)    # Move elbow from 90° to 180°
smooth_move(pen_servo, 45, 135)      # Move pen from 45° to 135°

# Return servos to a neutral position
smooth_move(shoulder_servo, 90, 0)
smooth_move(elbow_servo, 180, 90)
smooth_move(pen_servo, 135, 45)
