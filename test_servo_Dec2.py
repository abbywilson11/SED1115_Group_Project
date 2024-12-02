import math
from machine import Pin, PWM, ADC
import time

# Arm lengths
L1, L2 = 155, 155

# Function to compute inverse kinematics
def calculate_inverse_kinematics(Cx, Cy):
    """
    Calculate the joint angles (shoulder and elbow) for the robotic arm
    based on the target coordinates (Cx, Cy).
    """
    d = math.sqrt(Cx**2 + Cy**2)  # Distance from the base to the target

    if d > (L1 + L2) or d < abs(L1 - L2):
        # Point is unreachable
        return None, None

    # Calculate angles using the law of cosines
    cos_theta2 = (Cx**2 + Cy**2 - L1**2 - L2**2) / (2 * L1 * L2)
    theta2 = math.acos(cos_theta2)  # Elbow angle

    # Angle for the shoulder
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(Cy, Cx) - math.atan2(k2, k1)

    # Convert to degrees for servos
    servoA_angle = math.degrees(theta1)
    servoB_angle = math.degrees(theta2)

    return servoA_angle, servoB_angle

# Function to initialize the servos
def initialize_servo(pin_num):
    try:
        servo = PWM(Pin(pin_num))
        servo.freq(50)
        print(f"Servo initialized on Pin: {pin_num}")
        return servo
    except Exception as e:
        print(f"Error initializing servo on pin {pin_num}: {e}")
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
        print(f"Servo moved to {angle:.2f}° | Duty cycle: {duty}")
    except Exception as e:
        print(f"Error moving servo: {e}")

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

    # Paper boundaries (adjust based on the actual dimensions of your workspace)
    x_min, x_max = -150, 150
    y_min, y_max = 0, 200

    # Main loop to control servos based on potentiometer inputs
    while True:
        # Read potentiometer values
        x_value = x_pot.read_u16()
        y_value = y_pot.read_u16()

        # Map potentiometer values to coordinates
        x_coord = map_potentiometer_to_coordinates(x_value, pot_min, pot_max, coord_min, coord_max)
        y_coord = map_potentiometer_to_coordinates(y_value, pot_min, pot_max, coord_min, coord_max)

        print(f"Potentiometer values: X={x_value}, Y={y_value} | Coordinates: X={x_coord}, Y={y_coord}")

        # Check if the coordinates are within bounds
        if x_min <= x_coord <= x_max and y_min <= y_coord <= y_max:
            print("Coordinates are within bounds.")

            # Compute inverse kinematics
            angles = calculate_inverse_kinematics(x_coord, y_coord)
            if angles is None or None in angles:
                print("Point is unreachable, skipping...")
                continue

            shoulder_angle, elbow_angle = angles
            print(f"Target angles: Shoulder={shoulder_angle:.2f}°, Elbow={elbow_angle:.2f}°")

            # Move servos to calculated angles
            move_servo_to_angle(servo_shoulder, shoulder_angle)
            move_servo_to_angle(servo_elbow, elbow_angle)
        else:
            print("Coordinates are out of bounds. No movement performed.")

        time.sleep(0.2)  # Delay for smooth operation

except KeyboardInterrupt:
    print("Program terminated.")
