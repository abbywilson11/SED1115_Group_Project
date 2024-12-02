import math
from machine import Pin, PWM, ADC
import time

# Arm lengths
L1, L2 = 155, 155

# Function to compute inverse kinematics
def inverse_kinematics(x, y):
    """Compute shoulder (θ1) and elbow (θ2) angles for given (x, y) position."""
    d = math.sqrt(x**2 + y**2)
    if d > (L1 + L2):
        # Clamp the point to the reachable range
        x = x * (L1 + L2) / d
        y = y * (L1 + L2) / d
        d = L1 + L2

    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(cos_theta2) > 1:
        return None, None

    theta2 = math.acos(cos_theta2)
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    return math.degrees(theta1), math.degrees(theta2)

# Function to initialize the servos
def initialize_servo(pin_num):
    try:
        servo = PWM(Pin(pin_num))
        servo.freq(50)
        print("Servo initialized on Pin:", pin_num)
        return servo
    except Exception as e:
        print("Error initializing servo on pin", pin_num, ":", e)
        return None

# Function to translate an angle to a duty cycle
def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000
    duty_u16_value = int(duty_cycle * 65535)
    duty_u16_value = max(2300, min(7500, duty_u16_value))
    return duty_u16_value

# Function to move the servo to a specific angle
def move_servo_to_angle(servo, angle):
    if not servo:
        print("Error: Servo not initialized.")
        return
    
    angle = max(0, min(180, angle))
    duty = translate(angle)
    try:
        servo.duty_u16(duty)
        print(f"Servo moved to {angle}° | Duty cycle: {duty}")
    except Exception as e:
        print("Error moving servo:", e)

# Function to map potentiometer values to coordinates
def map_potentiometer_to_coordinates(value, min_val, max_val, min_coord, max_coord):
    """Map potentiometer values to coordinates."""
    return min_coord + (value - min_val) * (max_coord - min_coord) / (max_val - min_val)

# Main loop to control servos based on potentiometer inputs
try:
    # Initialize servos
    servo_shoulder = initialize_servo(0)  # Pin for shoulder joint
    servo_elbow = initialize_servo(1)    # Pin for elbow joint

    # Initialize potentiometers
    x_pot = ADC(Pin(26))  # Replace with the correct ADC pin for x-axis potentiometer
    y_pot = ADC(Pin(27))  # Replace with the correct ADC pin for y-axis potentiometer

    # Potentiometer input range (adjust based on actual hardware)
    pot_min, pot_max = 0, 65535

    # Coordinate range (workspace of the arm)
    coord_min, coord_max = -310, 310  # Adjust based on arm reach

    while True:
        # Read potentiometer values
        x_value = x_pot.read_u16()
        y_value = y_pot.read_u16()

        # Map potentiometer values to coordinates
        x_coord = map_potentiometer_to_coordinates(x_value, pot_min, pot_max, coord_min, coord_max)
        y_coord = map_potentiometer_to_coordinates(y_value, pot_min, pot_max, coord_min, coord_max)

        print(f"Potentiometer values: X={x_value}, Y={y_value} | Coordinates: X={x_coord}, Y={y_coord}")

        # Compute inverse kinematics
        angles = inverse_kinematics(x_coord, y_coord)
        if angles is None or None in angles:
            print("Skipping unreachable point.")
            continue

        shoulder_angle, elbow_angle = angles
        print(f"Target angles: Shoulder={shoulder_angle:.2f}°, Elbow={elbow_angle:.2f}°")

        # Move servos to calculated angles
        move_servo_to_angle(servo_shoulder, shoulder_angle)
        move_servo_to_angle(servo_elbow, elbow_angle)

        time.sleep(0.2)  # Delay for smooth operation

except KeyboardInterrupt:
    print("Program terminated.")
