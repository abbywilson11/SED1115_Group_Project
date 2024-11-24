import time
from machine import ADC, Pin, PWM

# Initialize servos
shoulder_servo = PWM(Pin(15))
elbow_servo = PWM(Pin(16))
pen_control_servo = PWM(Pin(17))

# Set PWM frequency for servos
shoulder_servo.freq(50)
elbow_servo.freq(50)
pen_control_servo.freq(50)

# Initialize potentiometers
x_pot = ADC(Pin(26))
y_pot = ADC(Pin(27))

# Initialize buttons
sw3 = Pin(12, Pin.IN, Pin.PULL_DOWN)
sw2 = Pin(11, Pin.IN, Pin.PULL_DOWN)

# State variables
pen_state = True
position_reset = False

def read_potentiometers():
    return x_pot.read_u16(), y_pot.read_u16()

def check_pen_control():
    global pen_state
    if sw3.value() == 1:
        pen_state = not pen_state
        print("Pen is Up" if pen_state else "Pen is Down")
    return pen_state

def check_reset():
    global position_reset
    if sw2.value() == 1:
        position_reset = True
        print("Position Reset")
    return position_reset

def set_servo_positions(x_pos, y_pos):
    shoulder_servo.duty_u16(x_pos)
    elbow_servo.duty_u16(y_pos)

def initialize():
    print("Initialization complete: Pico is ready for servo control.")

# Example usage
if __name__ == "__main__":
    initialize()
    while True:
        x_pos, y_pos = read_potentiometers()
        pen_state = check_pen_control()
        reset_state = check_reset()
        set_servo_positions(x_pos, y_pos)
        print(f"Potentiometer X-axis: {x_pos}, Potentiometer Y-axis: {y_pos}")
        time.sleep(0.05)