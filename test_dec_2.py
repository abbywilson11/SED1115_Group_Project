from machine import Pin, PWM
from adc import *
import time

def init_servo(pin):
    try:
        servo = PWM(Pin(pin), freq=50)
        print(f"Servo initialized on pin {pin}")
        return servo
    except Exception as e:
        print(e)
        return None
    
def convert_encoder_to_servo(shoulder, elbow):
    shoulder = int(shoulder * 0.75)
    elbow = 180 - elbow

    print(f"Converted Encoder Angles: {shoulder}, {elbow}")
    
def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000
    duty_u16_value = int(duty_cycle * 65535)
    duty_u16_value = max(2300, min(7500, duty_u16_value))
    return duty_u16_value

def move_servo(servo, angle):
    if not servo:
        print("Error: Servo not initialized.")
        return
    
    angle = max(0, min(215, angle))
    duty = translate(angle)
    try:
        servo.duty_u16(duty)
        print(f"Servo moved to {angle:.2f}° | Duty cycle: {duty}")
    except Exception as e:
        print(f"Error moving servo: {e}")

def map_linear_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def read_potentiometers(pot1_pin, pot2_pin):
    pot1 = ADC(Pin(pot1_pin))
    pot2 = ADC(Pin(pot2_pin))

    return pot1.read_u16(), pot2.read_u16()
    
def pots_to_coords(pot1, pot2, x_min=-310, x_max=310, y_min=-310, y_max=310):
    x_coord = map_linear_range(pot1, 0, 65535, x_min, x_max)
    y_coord = map_linear_range(pot2, 0, 65535, y_min, y_max)

    return x_coord, y_coord

def get_encoder_feedback():
    shoulder_encoder = adc.read(0, ADS1015_A_FB)
    elbow_encoder = adc.read(0, ADS1015_B_FB)

    shoulder_angle = map_linear_range(shoulder_encoder, 292, 1092, 0, 215)
    elbow_angle = map_linear_range(elbow_encoder, 942, 305, 0, 180)

    print(f"Encoder Angle: {shoulder_angle} {elbow_angle}")
    convert_encoder_to_servo(shoulder_angle, elbow_angle)

while True:
    servo_s = init_servo(0)
    servo_e = init_servo(1)
    pot1, pot2 = read_potentiometers(26, 27)
    shoulder, elbow = pots_to_coords(pot1, pot2, 0, 360, 0, 180)

    print(f"Target Angles: {shoulder}, {elbow}")
    get_encoder_feedback()

    move_servo(servo_s, shoulder)
    move_servo(servo_e, elbow)

    time.sleep(1)