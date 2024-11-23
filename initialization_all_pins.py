# This code is licensed under the MIT License, and Apache License
# machine by Raspberry Pi Ltd. 4.0 International Licence 
# TIME by Nicholas Delinte. GNU General Public License v3.0

"""
In my code, I basically initalized all the pins that we will need in our program :
1. X-Axis knob 
2. Y-Axis Knob
3. Pen Up/Down Control Button
4. Reset Button

It also prints the raw values for the X-Axis and Y-Axis knobs which is useful when we will be 
transforming them into angles.

The buttons work since I incorporated the code from our Toggle exercice. Both Pen Control and Reset work perfectly.

I also wrote in the code, for the future of the project, home positions for the x-axis and y-axis that the arm will go back to after
the reset button being pressed.

It also tracks the state of the buttons (Pen Control Up/Down Button and the Reset Button).
Each time they get pressed, it prints an indicator of the state so we know what is their current state (Up/Down)(Position Reset)

Lastely, it prints the values of each x and y axis knobs for debugging purposes.
"""


import time
from machine import ADC, Pin, PWM

# Initialize the Pins that will be used
shoulder_servo = PWM(Pin(15))
elbow_servo = PWM(Pin(16))
pen_control_servo = PWM(Pin(17))  # Example pin for pen up/down control

# Set PWM frequency for each servo (typically 50 Hz for standard servos)
shoulder_servo.freq(50)
elbow_servo.freq(50)
pen_control_servo.freq(50)

# Initialize analog inputs for X and Y potentiometers (ADC pins)
x_pot = ADC(Pin(26))  # GPIO pin for X-axis input
y_pot = ADC(Pin(27))  # GPIO pin for Y-axis input

# Initialize button values for pen control
sw3 = Pin(12, Pin.IN, Pin.PULL_DOWN)  # Pen control pin initialization
pcontrol_old_value = False  # Initial state value of old value of the pen control button
pcontrol_new_value = False  # Initial state value of new value of the pen control button

# Reset button / switch initialization
sw2 = Pin(11, Pin.IN, Pin.PULL_DOWN)  # Reset button pin initialization
reset_old_value = False  # Initial state value of old value of the reset button
reset_new_value = False  # Initial state value of new value of the reset button

# State variable to track pen position (True = Pen Up, False = Pen Down)
pen_state = True

# State variable for reset (to be used later)
position_reset = False

# initial position for both axis (x and y)
#home_position_x = ...  
#home_position_y = ...  

# Basic initialization print to confirm setup
print("Initialization complete: Pico is ready for servo control.")

while True:
    # Update the old and new values for the pen control button
    pcontrol_old_value = pcontrol_new_value
    pcontrol_new_value = sw3.value()

    # Check if pen control button was pressed (transition from 0 to 1)
    if pcontrol_new_value == 1 and pcontrol_old_value == 0:
        # Toggle pen state
        pen_state = not pen_state
        
        if pen_state:
            print("Pen is Up")
        else:
            print("Pen is Down")
    
    # Update the old and new values for the reset button
    reset_old_value = reset_new_value
    reset_new_value = sw2.value()

    # Check if reset button was pressed (transition from 0 to 1)
    if reset_new_value == 1 and reset_old_value == 0:
        # Set position reset state
        position_reset = True
        print("Position Reset")

    # If the reset state is active, you can add actions like resetting servo positions or other variables
    if position_reset:

        """
        This will be the place where we put the inital position of the arm so when
        we press the reset button, the arm replaces itself to that specific position.

        shoulder_servo.duty_u16(home_position_x)
        elbow_servo.duty_u16(home_position_y)
        print("Returning to home position")

        """

        # Reset the position_reset state for the next press
        position_reset = False

    # Read the position values from the potentiometers
    position_x = x_pot.read_u16()  # X-axis potentiometer value (0-65535)
    position_y = y_pot.read_u16()  # Y-axis potentiometer value (0-65535)
    
    # Set the duty cycle based on potentiometer readings
    shoulder_servo.duty_u16(position_x)
    elbow_servo.duty_u16(position_y)
    
    # Print the raw analog values for DEBUGGING
    print(f"Potentiometer X-axis : {position_x}, Potentiometer Y-axis : {position_y}")
    time.sleep_ms(500) # FOR DEBUGGING This makes it so it delays half a second between each print to be able to see more easily what is being printed

    # Small delay to debounce the button without affecting servo control or potentiometer readings
    time.sleep_ms(50)
