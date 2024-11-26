# The goal of this code is to detect a switch input that controls the pen's up and down movements
# When the switch is pressed, the pen should either raise or lower based on it's current position

import machine
import time

# Initialize the GPIO for the pen control switch
# We will use sw5 connected to GP22 since it is central to both the knobs and in an ideal position for the user
def pen_switch():

    switch = machine.Pin(22,machine.Pin.IN, machine.Pin.PULL_DOWN) # pull-down makes sure the switch reads 0 or LOW when not pressed

# Now to track the state changes (up or down), need to use a while loop to test continuously

    pen_down = False  # Assume the pen starts in the up position

    while True:
        if switch.value() == 1:  # If pen switch is pressed
        # Toggle pen state
            pen_down = not pen_down
        
        if pen_down:
            print("Pen Down")
        else:
            print("Pen Up")

        time.sleep(0.2)  # Adjust debounce time as needed for stability

        time.sleep(0.05)  # Main loop delay for checking state of switch

