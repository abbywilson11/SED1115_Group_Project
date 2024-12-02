import machine
import time

# Initialize the GPIO for the pen control switch and servo
def initialize_pen():
    # Configure the switch on GP22 (pull-down resistor for stability)
    pen_switch = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)
    # Configure the pen servo on pin 2
    pen_servo = machine.PWM(machine.Pin(2))
    pen_servo.freq(50)  # Typical frequency for servos
    return pen_switch, pen_servo

# Function to toggle pen state using the switch
def toggle_pen(pen_switch, pen_servo, pen_down):
    if pen_switch.value() == 1:  # If the switch is pressed
        pen_down = not pen_down  # Toggle the pen state
        time.sleep(0.2)  # Debounce delay for stable operation

    # Move the servo based on the state of pen_down
    if pen_down:
        pen_servo.duty_u16(4500)  # Adjust for "pen down" position (example value)
        print("Pen Down")
    else:
        pen_servo.duty_u16(7500)  # Adjust for "pen up" position (example value)
        print("Pen Up")

    return pen_down
