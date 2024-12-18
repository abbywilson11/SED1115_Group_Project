import machine
import time

def dont_run(): 
    raise Exception("oh no i ran it")

# Initialize/setup the ADC pins
x_pin = 27
y_pin = 26

def read_and_convert_knob_values(x_pin, y_pin, reset_flag):
    """
    Ownership: Antoine Boult and Calib Wong

    Reads potentiometer values from the given ADC pins and converts them to angles.

    Args:
        x_pin (int): GPIO pin number for the x-axis knob.
        y_pin (int): GPIO pin number for the y-axis knob.
        reset_flag (bool): Indicates whether the system is in reset mode.

    Returns:
        tuple: Raw knob values, angles (x_angle, y_angle), and reset_flag status.
    """
    x_knob = machine.ADC(x_pin)
    y_knob = machine.ADC(y_pin)

    # Read knob values
    x_value = x_knob.read_u16()
    y_value = y_knob.read_u16()

    # Check for reset condition
    if reset_flag:
        # Wait for both knobs to return to 0 position (low values)
        if x_value < 200 and y_value < 200:
            print("Knobs returned to 0. Resuming normal operation.")
            reset_flag = False  # Exit reset mode
        else:
            print(f"To move again, bring both knobs to 0 | Current Values: x-knob: {x_value}, y-knob: {y_value}")
            return x_value, y_value, 0, 0, reset_flag

    """

    Handeling the invalid values 

    Intentional decision : didn't put 176 since sometimes it went down to 160 and brang back to home position a lot of times
    I put it to 160 to make it so the experience is better because it doesn't bring it back to home position anymore for a noise issue like that
    Smooths out the experience.
    
    Did the same thing for the highest value possible with the pins. I didn't put it at 65535 I wanted to widen the margin so I put to 65550

    """

    # Intentional decision : didn't put 176 since sometimes it went down to 160 and brang back to home position a lot of times
    if x_value > 65550 or y_value > 65550 or x_value < 160 or y_value < 160: 
        print(f"Resetting to home position due to invalid values. Current knobs: x={x_value}, y={y_value}")
        reset_flag = True
        return x_value, y_value, 0, 0, reset_flag

    # Convert knob values to angles
    x_angle = int((x_value * 180) / 65535)
    y_angle = int((y_value * 180) / 65535)

    return x_value, y_value, x_angle, y_angle, reset_flag


# Initialize reset flag
reset_flag = False

# while True:
#     # Read knob values and process angles
#     x_value, y_value, x_angle, y_angle, reset_flag = read_and_convert_knob_values(x_pin, y_pin, reset_flag)

#     # Print the raw values and corresponding angles
#     print(f"x knob: {x_value} to {x_angle} angle, y knob: {y_value} to {y_angle} angle")
# dont_run()
#     time.sleep(0.05)  # Small delay for smoother updates
