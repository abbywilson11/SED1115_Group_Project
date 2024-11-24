# This code is licensed under the MIT License, and Apache License
# machine by Raspberry Pi Ltd. 4.0 International Licence 
# TIME by Nicholas Delinte. GNU General Public License v3.0

# Etch-A-Sketch Program: Combines knob (x and y axis) reading, pen switch control, and voltage verification

#import libraries 
import machine
import time
import utime

#imported code that defines all of our pins 
import initialization_all_pins

# ADC Voltage Calculation 
def adc_voltage(adc_value):
    return (adc_value / 65535) * 3.3  # Convert ADC reading to voltage (assuming a 3.3V Pico)

def verify_input(value, min_value, max_value):
    return min_value <= value <= max_value

# Initialize ADC for X and Y Knobs 
x_knob = machine.ADC(27)  # X-axis potentiometer
y_knob = machine.ADC(26)  # Y-axis potentiometer

# Initialize GPIO for Pen Switch 
pen_switch = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Pen control switch
pen_down = False  # Initial pen position is up

try:
    while True:
        # Read X and Y Knob Values
        x_value = x_knob.read_u16()
        y_value = y_knob.read_u16()

        # Calculate and display voltage for X and Y
        x_voltage = adc_voltage(x_value)
        y_voltage = adc_voltage(y_value)
        
        # Verify the input voltage range and display the values
        if verify_input(x_voltage, 0, 3.3) and verify_input(y_voltage, 0, 3.3):
            print(f"X-Axis Voltage: {x_voltage:.2f}V (Raw: {x_value}), Y-Axis Voltage: {y_voltage:.2f}V (Raw: {y_value})")
        else:
            print(f"Error: Input out of expected range (X Raw: {x_value}, Y Raw: {y_value})")

        # Pen Toggle based on Switch State
        if pen_switch.value() == 1:  # If pen switch is pressed
            # Toggle pen state
            pen_down = not pen_down
            print("Pen Down" if pen_down else "Pen Up")
            time.sleep(0.2)  # Debounce delay

        # Main loop delay (to stabilize readings)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nProgram terminated by user")

