# This code is licensed under the MIT License, and Apache License
# machine by Raspberry Pi Ltd. 4.0 International Licence 
# TIME by Nicholas Delinte. GNU General Public License v3.0

# import specific parts of the library, not the whole thing for machine
import utime
from machine import Pin, ADC 

# Initialize ADC to read the analog signal
adc = ADC(Pin(26)) #connected to pin 26

# convert the raw ADC value into a voltage value 
def adc_voltage(adc_value):
    return (adc_value / 65535) * 3.3 # this is the assumed voltage of a pico

# verify the input value 
def verify_input(value, min_value, max_value):
    return min_value <= value <= max_value

try: 
    while True: 
        raw_value = adc.read_u16() # read analog value 
        voltage = adc_voltage(raw_value) # convert to voltage 

        if verify_input(voltage, 0, 3.3):
            # verify the input, then print the values of raw and voltage
            print(f"Analog input: {voltage:.2f}V (Raw:{raw_value})")
        else: # handle if value is out of wanted range 
            print(f"Error: Input out of expected range (Raw: {raw_value})")
        
        utime.sleep(1)

# create an exception, when the user does a keyboard iterupptoon it shuts down the program
except KeyboardInterrupt:
    print("\nProgram terminated by user")