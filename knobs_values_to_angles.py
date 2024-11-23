import machine
import time

# Initialize/setup the ADC pins
x_pin = 27
y_pin = 26

def read_and_convert_knob_values(x_pin, y_pin, last_valid_x_angle, last_valid_y_angle):
    """
    Ownership: Antoine Boult and Calib Wong

    It reads the values from the x and y axis knobs and converts them to angles. It also ensures that when
    the angles from either knobs is too low or too high, it brings it back to the home position which is both 90 degrees (Middle of the page)

    Issue resolved :
    It also ensures that it stays at the home position until you move the knobs again since when it comes back to 90 degrees, the knob are still 
    have the values / angles that they were in before so right after it's in the home position it goes back where it was. It is now smoothed out.

    Args:
        x_pin (int): GPIO pin number for the x-axis knob.
        y_pin (int): GPIO pin number for the y-axis knob.
        last_valid_x_angle (int): Last valid angle for the x-axis.
        last_valid_y_angle (int): Last valid angle for the y-axis.

    Returns:
        tuple: (x_value, y_value, x_angle, y_angle)
        - Raw knob values and angles scaled from 0 to 180 degrees. If values are invalid,
          the function returns the home position and retains the last valid angles.
    """

    x_knob = machine.ADC(x_pin)
    y_knob = machine.ADC(y_pin)

    # Read values
    x_value = x_knob.read_u16()
    y_value = y_knob.read_u16()

    # Error handling: Keep angles at 90 degrees (home position) if values are invalid
    if x_value < 176 or y_value < 176:
        print("Values too low. Holding at home position.")
        return x_value, y_value, 90, 90

    if x_value > 65535 or y_value > 65535:
        print("Values too high. Holding at home position.")
        return x_value, y_value, 90, 90

    # Scale values to angles
    x_angle = int((x_value * 180) / 65535)
    y_angle = int((y_value * 180) / 65535)

    # If angles are valid, return them
    return x_value, y_value, x_angle, y_angle

# Initialize last valid angles
last_valid_x_angle = 90
last_valid_y_angle = 90


# Need to add these parts to the main code
while True:
    # Get the raw values and angles from the function
    x_value, y_value, x_angle, y_angle = read_and_convert_knob_values(x_pin, y_pin, last_valid_x_angle, last_valid_y_angle)

    # If the angles are valid (not 90 due to an error), update the last valid angles
    if x_angle != 90 or y_angle != 90:
        last_valid_x_angle = x_angle
        last_valid_y_angle = y_angle

    # Print the raw values and corresponding angles
    print(f"x knob: {x_value} to {x_angle} angle, y knob: {y_value} to {y_angle} angle")

