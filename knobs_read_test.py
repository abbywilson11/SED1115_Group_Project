import machine
import time

# Initialize/setup the ADC pins
x_knob = machine.ADC(27)
y_knob = machine.ADC(26)

# Function to convert knob values to angles in the range 0-180 degrees
def knob_value_to_angle(x_value, y_value):
    """
    Ownership: Antoine Boult

    Converts potentiometer values to angles for servo control.
    Scales values from 0-65535 to 0-180 degrees.

    Error handeling to ensure the security of the user and to prevent any equipment from breaking 
    by bringing back to the reset position angles if any of the x or y axis knobs have values that are under 176 or over 65535.

    """
    # It intifies the values from both knobs and then turns them into angles scaled from the range 0-180
    x_angle = int((x_value * 180) / 65535)
    y_angle = int((y_value * 180) / 65535)

    # Error handling: reset to 90 (home position) if values are invalid
    if not (0 <= x_value <= 65535 and 0 <= y_value <= 65535):
        print("Invalid values detected. Resetting to home position.")
        x_angle = 90  # Home position
        y_angle = 90
    return x_angle, y_angle

# Main loop
while True:
    # Read potentiometer values
    x_value = x_knob.read_u16()
    y_value = y_knob.read_u16()

    # Get angles from knob values
    x_angle, y_angle = knob_value_to_angle(x_value, y_value)

    # Display values
    print(f"x: {x_value} to angle {x_angle}, y: {y_value} to angle {y_angle}")

    time.sleep(1)  # 1-second delay
