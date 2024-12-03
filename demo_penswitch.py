from machine import Pin, PWM
import time

# Initialize pen switch input pin
pen_switch_pin = Pin(22, Pin.IN)  # GPIO 15 as an input for pen switch

# Initialize pen servo
pen_servo_pin = 2  # GPIO pin for the pen servo
servo = PWM(Pin(pen_servo_pin))
servo.freq(50)  # Set servo PWM frequency to 50Hz

# Translate angle to duty cycle
def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000
    duty_u16_value = int(duty_cycle * 65535)
    return max(2300, min(7500, duty_u16_value))

# Move servo to a specific angle
def move_servo_to_angle(angle):
    duty = translate(angle)
    servo.duty_u16(duty)
    print(f"Pen servo moved to {angle:.2f}° | Duty cycle: {duty}")

# Check pen switch state and move the pen
def pen_switch_loop():
    """
    Continuously monitor the pen switch state.
    If the switch indicates 'down', move the pen down; otherwise, move it up.
    """
    print("got here 0")
    try:
        print("got here 1")
        last_state = False 
        while True:
            state = last_state
            state = state ^ pen_switch_pin.value() # uses XOR operation to invert the state when the button is pressed
            print(f"State: {state} | LS: {last_state}")
            if state != last_state:
                if state:
                    #move_servo_to_angle(0)  # Pen down position
                    servo.duty_u16(3000)
                    print("Pen is down.")
                else:
                    #move_servo_to_angle(-30)  # Pen up position
                    servo.duty_u16(2300)
                    print("Pen is up.")
                last_state = state
            time.sleep(0.3)  # Add a short delay to prevent excessive checks
    except KeyboardInterrupt:
        print("Pen switch loop terminated.")


pen_switch_loop()