# The purpose of this code is to allow for accurate motion control of the servos

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


# define a function that will move the servo to a specific angle
def move_servo_to_angle(servo, angle): # servo is of type PWM (controlling the servo) and angle is of type int (target angle servo moves to)

    #  check to see if angle is within the desired range
    if angle < 0:
        # moves the value to the nearest available value within the upper and lower limits (0-180 degrees)
        print("Error: Angle is too low! Setting angle to 0 degrees.")
        angle = 0
    elif angle > 180:
        print("Error: Angle is too high! Setting angle to 180 degrees.")

    # maps the angle to a duty cycle (research typical ranges for better idea)
    min_duty_cycle = 1000 # matches with 0 degrees lower limit
    max_duty_cyle = 9000 # matches with 180 degrees upper limit

    # calculated duty cycle
    duty = int(min_duty_cycle + (angle/180) * (max_duty_cyle-min_duty_cycle))

    # check to see if duty cycle is within range by clamping to limits
    if duty < min_duty_cycle:
        duty = min_duty_cycle
        print("The duty cyle has been set to a minimum value.")
    
    elif duty > max_duty_cyle:
        duty = max_duty_cyle
        print("The duty cyle has been set to a maximum value.")

    # sends the duty cycle to the servo
    servo.duty_u16(duty)

# define a function that warns if the servos are overheating due to continuous use
servo_start_time = time.time() # begins to track time when the servo starts moving

def check_servo_usage():
    elapsed_time = time.time() - servo_start_time # calculates how long the servo has been active

    if elapsed_time > 30: # if the servo runs for more than 30 seconds, a warning is given
        print("Warning! Servo might be overheating, give it a rest!") 
        time.sleep(10) # pauses the program to allow for a 10 second cooldown

