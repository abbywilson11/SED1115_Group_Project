'''# The purpose of this code is to allow for accurate motion control of the servos

# import the required modules that will be used
from machine import Pin, PWM
import time

# define a function that initializes the servos based on the selected GPIO pin
def initialize_servo(pin_num): # pin_num is of type int and represents the GPIO pin that the servo is connected to
    
    # check if the PWM object is set up correctly during initialization
    try: 
        servo = PWM(Pin(pin_num)) # converts the GPIO pin to a PWM pin
        servo.freq(100) # sets the servo frequency to 100 Hz but needs to be changed based on servo standard!
        print("Servo initialized on Pin:", pin_num)
        
        return servo # should expect to return a PWM object for controlling the servo
    
    except Exception as e: # catches any errors and prints a message to user
        print("Error initialzing servo on pin ", pin_num, ":", e)
        
        return None

# translate function for angle-to-duty cycle conversion
def translate(angle: float) -> int:
    # Converts angle to PWM in microseconds
    pulse_width = 500 + (2500 - 500) * angle / 180  # Typical servo range: 500us (0°) to 2500us (180°)
    
    # Calculates duty cycle for 20ms period
    duty_cycle = pulse_width / 20000
    
    # Scales to 16-bit value and clamp to safe limits
    duty_u16_value = int(duty_cycle * 65535)
    duty_u16_value = max(2300, min(7500, duty_u16_value))  # Clamp between safe limits
    
    return duty_u16_value

# define a function that will move the servo to a specific angle
def move_servo_to_angle(servo, angle): # servo is of type PWM (controlling the servo) and angle is of type int (target angle servo moves to)

    # check to see if the servo can move to the angle or if it is connected properly
    if not servo:
        print("Error: Servo not initialized. Cannot move to angle.")
        return
    
    # check to see if angle is within the desired range
    if angle < 0:
        # moves the value to the nearest available value within the upper and lower limits (0-180 degrees)
        print("Error: Angle is too low! Setting angle to 0 degrees.")
        angle = 0
    elif angle > 180:
        print("Error: Angle is too high! Setting angle to 180 degrees.")
        angle = 180

    # Calculates duty cycle using the translate function
    duty = translate(angle)

    # maps the angle to a duty cycle (research typical ranges for better idea)
    # min_duty_cycle = 1000 # matches with 0 degrees lower limit
    # max_duty_cyle = 9000 # matches with 180 degrees upper limit

    # calculated duty cycle
    # duty = int(min_duty_cycle + (angle/180) * (max_duty_cyle-min_duty_cycle))

    # check to see if duty cycle is within range by clamping to limits
    # if duty < min_duty_cycle:
        # duty = min_duty_cycle
        # print("The duty cyle has been set to a minimum value.")
    
    # elif duty > max_duty_cyle:
        # duty = max_duty_cyle
        # print("The duty cyle has been set to a maximum value.")


    # duty = translate(angle)
    # def translate (angle: float) -> int:
    # pulse_width = 500 + (2500-500) * angle / 180 #pulse width equation
    # duty_cycle = pulse_width / 20000 # 20000 microseconds / 20ms
    # duty_u16_value = int(duty_cycle * 65535) # multiply so it is in pwm class
    # duty_u16_cycle = max(2300, min(7500, duty_u16_value)) # clamps down value
    # return duty_u16_value


    # sends the duty cycle to the servo
    try:
        servo.duty_u16(duty)
        print("Servo moved to", angle, "degrees", "Duty cycle is: ", duty)
    except Exception as e:
        print("Error moving servo: ", e)

# define a function that warns if the servos are overheating due to continuous use
# start_time = time.time() # begins to track time when the servo starts moving

def check_servo_usage(start_time):
    elapsed_time = time.time() - start_time # calculates how long the servo has been active

    if elapsed_time > 30: # if the servo runs for more than 30 seconds, a warning is given
        print("Warning: Servo might be overheating, give it a rest!") 
        time.sleep(10) # pauses the program to allow for a 10 second cooldown '''

# import the required modules
from machine import Pin, PWM, ADC
import time

# Function to initialize the servos
def initialize_servo(pin_num):
    try:
        servo = PWM(Pin(pin_num))  # Initialize PWM on the given pin
        servo.freq(50)  # Typical servo frequency is 50Hz
        print("Servo initialized on Pin:", pin_num)
        return servo
    except Exception as e:
        print("Error initializing servo on pin", pin_num, ":", e)
        return None

# Function to translate an angle to a duty cycle
def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180  # 0° = 500us, 180° = 2500us
    duty_cycle = pulse_width / 20000  # Convert to a fraction of 20ms
    duty_u16_value = int(duty_cycle * 65535)  # Scale to 16-bit
    duty_u16_value = max(2300, min(7500, duty_u16_value))  # Clamp to safe range
    return duty_u16_value

# Function to move the servo to a specific angle
def move_servo_to_angle(servo, angle):
    if not servo:
        print("Error: Servo not initialized.")
        return
    
    # Clamp angle to range 0–180
    angle = max(0, min(180, angle))
    duty = translate(angle)

    try:
        servo.duty_u16(duty)
        print(f"Servo moved to {angle}° | Duty cycle: {duty}")
    except Exception as e:
        print("Error moving servo:", e)

# define a function that warns if the servos are overheating due to continuous use
# start_time = time.time() # begins to track time when the servo starts moving

def check_servo_usage(start_time):
    elapsed_time = time.time() - start_time # calculates how long the servo has been active

    if elapsed_time > 30: # if the servo runs for more than 30 seconds, a warning is given
        print("Warning: Servo might be overheating, give it a rest!") 
        time.sleep(10) # pauses the program to allow for a 10 second cooldown 

# Function to read and convert potentiometer values to angles
def read_and_convert_knob_values(x_pin, y_pin):
    x_knob = ADC(Pin(x_pin))
    y_knob = ADC(Pin(y_pin))
    
    # Read knob values (range: 0–65535)
    x_value = x_knob.read_u16()
    y_value = y_knob.read_u16()
    
    # Map values to angles (range: 0–180)
    x_angle = int((x_value / 65535) * 180)
    y_angle = int((y_value / 65535) * 180)
    
    return x_angle, y_angle

# Main script
if __name__ == "__main__":
    # Initialize servos
    servo_x = initialize_servo(15)  # Replace with GPIO pin for x-axis servo
    servo_y = initialize_servo(16)  # Replace with GPIO pin for y-axis servo

    # Initialize potentiometer pins
    x_pot_pin = 26  # Replace with ADC pin for x-axis potentiometer
    y_pot_pin = 27  # Replace with ADC pin for y-axis potentiometer

    # Main loop to control servos using potentiometers
    try:
        while True:
            # Read potentiometer values and convert to angles
            x_angle, y_angle = read_and_convert_knob_values(x_pot_pin, y_pot_pin)

            # Move servos based on potentiometer input
            move_servo_to_angle(servo_x, x_angle)
            move_servo_to_angle(servo_y, y_angle)

            # Delay for smooth operation
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program terminated.")
