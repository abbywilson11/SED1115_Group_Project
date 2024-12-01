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
        print(f"Servo moved to {angle} | Duty cycle: {duty}")
    except Exception as e:
        print("Error moving servo:", e)

# Define a function that warns if the servos are overheating due to continuous use
def check_servo_usage(start_time):
    elapsed_time = time.time() - start_time  # Calculates how long the servo has been active

    if elapsed_time > 30:  # If the servo runs for more than 30 seconds, a warning is given
        print("Warning: Servo might be overheating, give it a rest!") 
        time.sleep(10)  # Pauses the program to allow for a 10-second cooldown 

# Main loop to control servos using potentiometers
try:
    # Initialize servos
    servo_x = initialize_servo(0)  # Replace with GPIO pin for x-axis servo
    servo_y = initialize_servo(1)  # Replace with GPIO pin for y-axis servo

    # Initialize potentiometer pins
    x_pot_pin = 26  # Replace with ADC pin for x-axis potentiometer
    y_pot_pin = 27  # Replace with ADC pin for y-axis potentiometer
    
    x_knob = ADC(Pin(x_pot_pin))  # Initialize ADC for x-axis potentiometer
    y_knob = ADC(Pin(y_pot_pin))  # Initialize ADC for y-axis potentiometer

    start_time = time.time()  # Start time for servo usage

    while True:
        # Read potentiometer values directly
        x_value = x_knob.read_u16()
        y_value = y_knob.read_u16()

        # Map values to angles (range: 0–180)
        x_angle = int((x_value / 65535) * 180)
        y_angle = int((y_value / 65535) * 180)

        print(f"Potentiometer values: X={x_value}, Y={y_value} | Angles: X={x_angle}, Y={y_angle}")

        # Move servos
        move_servo_to_angle(servo_x, x_angle)
        move_servo_to_angle(servo_y, y_angle)

        # Check for overheating
        check_servo_usage(start_time)

        # Delay for smooth operation
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated.")
