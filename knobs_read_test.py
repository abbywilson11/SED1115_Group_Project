# The goal of this code is to test the accuracy of the analog input values from the two potentiometers
# The two potentiometers (knobs) represent the x and y axes
# These values will control the brachiographs 2D movements

import machine
import time

# left knob is A1/R2 meaning it is linked to GP27, we can assign this to x control
# right knbo is A0/R1 meaning it is linked to GP26, we can assign this to y control

# initialize/setup the ADC pins
x_knob = machine.ADC(27)
y_knob = machine.ADC(26)

# read and print values from the potentiometers
# ideally we want to encourage continuous testing instead of having to re-run th eprogram every time, thus while loop

while True:

    # returns a 16-bit integer value wrt position between 0 (min) and 65535 (max)
    x_value = x_knob.read_u16()
    y_value = y_knob.read_u16()

    print("x: ", x_value, "y: ", y_value) # displays potentiometer values

    time.sleep_ms(2222) # handles debouncing and improves stability

