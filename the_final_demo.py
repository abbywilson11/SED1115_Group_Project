# 2-joint robotic arm etch a sketch script
# import required libraries 
import math
from machine import Pin, PWM
from adc import * #file Knox provided
import time

# Arm lengths in millimeters
L1, L2 = 155, 155 # first and second armm segments 
last_state = bool(False) # beginning state for pen switch

def forward_kinematics(theta1, theta2):
    """Calculate the position of the end effector (x, y) using forward kinematics."""
    theta1 = math.radians(theta1) # angle of the shoulder joint
    theta2 = math.radians(theta2) # angle of the eblow joint

    x = (L1 * math.cos(theta1)) + (L2 * math.cos(theta1 + theta2))
    y = (L1 * math.sin(theta1)) + (L2 * math.sin(theta1 + theta2))
    return x, y

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
    theta1 = (math.atan2(Cy, Cx) - math.atan2(k2, k1)) % math.pi

    # Convert to degrees for servos
    servoA_angle = math.degrees(theta1) # shoulder angle
    servoB_angle = math.degrees(theta2) # elbow angle 

    return servoA_angle, servoB_angle

# Function to initialize the servos
def initialize_servo(pin_num):
    try:
        servo = PWM(Pin(pin_num))
        servo.freq(50) # frequency of 50 Hz (50 times a second)
        print(f"Servo initialized on Pin: {pin_num}")
        return servo
    except Exception as e: # error handling 
        print(f"Error initializing servo on pin {pin_num}: {e}")
        return None

# Function to translate a servo angle to a 16-bit duty cycle
def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180 # equation given in lab 5
    duty_cycle = pulse_width / 20000
    duty_u16_value = int(duty_cycle * 65535)
    duty_u16_value = max(2300, min(7500, duty_u16_value))
    return duty_u16_value

# Function to move the servo to a specific angle
def move_servo_to_angle(servo, angle):
    if not servo:
        print("Error: Servo not initialized.")
        return
    
    angle = max(0, min(215, angle)) #min and max angles for servo
    duty = translate(angle)
    try:
        servo.duty_u16(duty) # move servo to desired angle 
        print(f"Servo moved to {angle:.2f}° | Duty cycle: {duty}")
    except Exception as e: # handle servo movement errors, disconnected or invalid
        print(f"Error moving servo: {e}")

# Function to map potentiometer values to coordinates
def map_potentiometer_to_coordinates(value, min_val, max_val, min_coord, max_coord):
    """Map potentiometer values to coordinates."""
    return (value - min_val) * (max_coord - min_coord) / (max_val - min_val) + min_coord

def map_encoder_to_angle(input, min_enc, max_enc, min_angle, max_angle):
    return (input - min_enc) / abs(max_enc - min_enc) * abs(max_angle - min_angle) + min_angle

def validate_angles(angles, max_angle_shoulder, max_angle_elbow):
    shoulder, elbow = angles
    if shoulder is not None:
        if shoulder > max_angle_shoulder:
            shoulder = max_angle_shoulder
    if elbow is not None:
        if elbow > max_angle_elbow: 
            elbow = max_angle_elbow
    return shoulder, elbow

# read encoder feedback & calculate angles and end-effector coordinates
# monitor actual position of arm 
def get_encoder_feedback():
    shoulder_encoder = adc.read(0, ADS1015_A_FB)
    elbow_encoder = adc.read(0, ADS1015_B_FB)

    shoulder_current_angle = map_encoder_to_angle(
        shoulder_encoder,
        292,
        1092,
        0,
        215
    )

    elbow_current_angle = map_encoder_to_angle(
        elbow_encoder,
        942,
        305,
        0,
        180
    )

    # print(f"Raw Encoder Values: {shoulder_encoder} {elbow_encoder}")
    print(f"Encoder Angles: Shoulder={shoulder_current_angle}, Elbow={elbow_current_angle}")
    x, y = forward_kinematics(shoulder_current_angle, elbow_current_angle)
    print(f"Encoder Coordinates: X {x} - Y {y}")

def pen_position_check(servo, pen_switch_pin, last_state):
    button = pen_switch_pin.value()
    if (not button): return last_state
    state = last_state
    state = not state # inverts the state
    print(f"State: {state} | LS: {last_state}")
    if state:
        #move_servo_to_angle(0)  # Pen down position
        servo.duty_u16(3000)
        print("Pen is down.")
    else:
        #move_servo_to_angle(-30)  # Pen up position
        servo.duty_u16(2300)
        print("Pen is up.")
    last_state = state

    time.sleep(0.5)
    
    return state

# Main loop to control servos based on potentiometer inputs
try:
    # Initialize servos
    servo_shoulder = initialize_servo(0)  # Pin for shoulder joint
    servo_elbow = initialize_servo(1)    # Pin for elbow joint
    servo_pen = initialize_servo(2)     # Pin for pen joint

    # Initialize pin button
    pen_switch_pin = Pin(22, Pin.IN)

    # Initialize potentiometers
    x_pot = ADC(Pin(26))  # Replace with the correct ADC pin for x-axis potentiometer
    y_pot = ADC(Pin(27))  # Replace with the correct ADC pin for y-axis potentiometer

    # Potentiometer input range (adjust based on actual hardware)
    pot_min, pot_max = 0, 65535

    # Coordinate range (workspace of the arm)
    coord_min, coord_max = -310, 310  # Adjust based on arm reach

    # Paper boundaries (adjust based on the actual dimensions of your workspace)
    x_min, x_max = -290, -70
    y_min, y_max = -110, 120

    # initialize pen state
    state = False

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
        # if True:
            print("Coordinates are within bounds.")

            # Compute inverse kinematics
            angles = calculate_inverse_kinematics(x_coord, y_coord)
            if angles is None or None in angles:
                print("Point is unreachable, skipping...")
                continue

            shoulder_angle, elbow_angle = angles
            
            get_encoder_feedback() 

            if (shoulder_angle): shoulder_angle = shoulder_angle * 0.8
            if (elbow_angle): elbow_angle = 180 - elbow_angle

            angles = shoulder_angle, elbow_angle

            # angles = validate_angles(angles, 360, 180)

            shoulder_angle, elbow_angle = angles

            print(f"Target angles: Shoulder={shoulder_angle}°, Elbow={elbow_angle}°")

            # Move servos to calculated angles
            move_servo_to_angle(servo_shoulder, shoulder_angle)
            move_servo_to_angle(servo_elbow, elbow_angle)

            state = pen_position_check(servo_pen, pen_switch_pin, state)
        else:
            print("Coordinates are out of bounds. No movement performed.")

        time.sleep(0.01)  # Delay for smooth operation

# exit program when the user interrupts 
except KeyboardInterrupt: 
    print("Program terminated.")
