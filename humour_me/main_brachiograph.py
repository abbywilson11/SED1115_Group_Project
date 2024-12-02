# main.py
import time
from pen_toggle import initialize_pen, toggle_pen
from adc_input import read_adc_value
from ik import calculate_inverse_kinematics
from control_servo import move_servo, initialize_servo

# Initialize the components
pen_switch, pen_servo = initialize_pen()  # Initialize pen control
shoulder_servo = initialize_servo(0)      # Initialize shoulder servo on pin 0
elbow_servo = initialize_servo(1)         # Initialize elbow servo on pin 1
pen_down = False                          # Pen starts in the up position

# Initialize current angles for the servos
current_shoulder_angle = 90  # Starting at 90 degrees for the shoulder
current_elbow_angle = 90     # Starting at 90 degrees for the elbow

# Main program loop
while True:
    # Read ADC values for potentiometers (shoulder and elbow)
    shoulder_value = read_adc_value(0)  # Read the ADC value for the shoulder potentiometer
    elbow_value = read_adc_value(1)     # Read the ADC value for the elbow potentiometer

    # Map the ADC values (0-4095) to X, Y coordinates for the drawing surface
    x = shoulder_value / 4095 * 100  # Example mapping
    y = elbow_value / 4095 * 100     # Example mapping

    # Calculate inverse kinematics to get the angles for the shoulder and elbow servos
    alpha, beta = calculate_inverse_kinematics(x, y)

    # Smoothly move the servos based on the calculated angles
    current_shoulder_angle = move_servo(shoulder_servo, alpha, current_shoulder_angle)  # Move shoulder servo to 'alpha' angle
    current_elbow_angle = move_servo(elbow_servo, beta, current_elbow_angle)      # Move elbow servo to 'beta' angle
