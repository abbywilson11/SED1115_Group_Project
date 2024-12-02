from machine import Pin, PWM
import time

def initialize_servo(pin_number):
    """
    Initialize a servo on a given pin.
    """
    servo = PWM(Pin(pin_number))
    servo.freq(50)  # Standard frequency for servos
    print(f"Servo initialized on pin {pin_number}")
    return servo

def angle_to_duty_cycle(angle):
    """
    Convert angle (0-180 degrees) to duty cycle for PWM.
    """
    min_pulse = 500  # Minimum pulse width in microseconds
    max_pulse = 2500  # Maximum pulse width in microseconds
    pulse_width = min_pulse + (max_pulse - min_pulse) * angle / 180
    duty_cycle = int((pulse_width / 20000) * 65535)
    return max(2300, min(7500, duty_cycle))  # Clamp duty cycle

def move_servo(servo, target_angle, current_angle, step=1, delay=0.01):
    """
    Smoothly move a servo to the target angle.
    """
    if current_angle < target_angle:
        step = abs(step)
    else:
        step = -abs(step)
    
    while current_angle != target_angle:
        current_angle += step
        if abs(current_angle - target_angle) < abs(step):
            current_angle = target_angle
        servo.duty_u16(angle_to_duty_cycle(current_angle))
        time.sleep(delay)
    return current_angle

if __name__ == "__main__":
    servo_test = initialize_servo(0)
    current_angle = 90
    target_angle = 45
    current_angle = move_servo(servo_test, target_angle, current_angle)
