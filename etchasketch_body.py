# how to move arms: shoulder and elbow are two motors. 
# the same angle that our shoulder moves, our elbow moves but negatively (inverse) 
# switch each depending on x and y
import machine
import time
from servo_control import *
from inverse_kinematics import *

# ADC Voltage Calculation
def adc_voltage(adc_value):
    return (adc_value / 65535) * 3.3  # Convert ADC reading to voltage (assuming a 3.3V Pico)

def verify_input(value, min_value, max_value):
    return min_value <= value <= max_value

def main():
    # Initialize ADC for X and Y Knobs
    x_knob = machine.ADC(27)  # X-axis potentiometer
    y_knob = machine.ADC(26)  # Y-axis potentiometer

    # Initialize GPIO for Pen Switch
    pen_switch = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Pen control switch
    pen_down = False  # Initial pen position is up
    time.sleep(2)  # 2-second delay for initialization

    try:
        while True:
            # Read X and Y Knob Values
            x_value = x_knob.read_u16()
            y_value = y_knob.read_u16()

            # Calculate voltage for X and Y
            x_voltage = adc_voltage(x_value)
            y_voltage = adc_voltage(y_value)

            # Check pen switch state
            if pen_switch.value() == 1:  # If the switch is pressed
                pen_down = not pen_down  # Toggle pen state
                print("Pen Down" if pen_down else "Pen Up")
                time.sleep(0.2)  # Debounce delay

            # Only print values if pen is down
            if pen_down:
                if verify_input(x_voltage, 0, 3.3) and verify_input(y_voltage, 0, 3.3):
                    print(f"X-Axis Voltage: {x_voltage:.2f}V (Raw: {x_value}), Y-Axis Voltage: {y_voltage:.2f}V (Raw: {y_value})")
                else:
                    print(f"Error: Input out of expected range (X Raw: {x_value}, Y Raw: {y_value})")

            time.sleep(0.02)  # Main loop delay

    except KeyboardInterrupt:
        print("\nProgram terminated by user")

# Run the main program
if __name__ == "__main__":
    main()
