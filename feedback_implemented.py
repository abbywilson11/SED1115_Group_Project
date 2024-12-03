import math
from machine import Pin, PWM, ADC, I2C
import time
from ads1x15 import ADS1015

# Constants for I2C pins and ADS1015 configuration
I2C_SDA = 14
I2C_SCL = 15
ADS1015_ADDR = 0x48
ADS1015_A_FB = 0  # Feedback for Servo A (shoulder)
ADS1015_B_FB = 1  # Feedback for Servo B (elbow)

# Robotic arm constants
L1, L2 = 155, 155

# Initialize I2C and ADS1015
i2c = I2C(1, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))
adc = ADS1015(i2c, ADS1015_ADDR, 1)

# Translate angle to duty cycle
def translate(angle):
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_u16_value = int((pulse_width / 20000) * 65535)
    return max(2300, min(7500, duty_u16_value))

# Move servo to angle
def move_servo(servo, angle):
    if servo:
        duty = translate(angle)
        servo.duty_u16(duty)

# Calculate inverse kinematics
def calculate_inverse_kinematics(Cx, Cy):
    d = math.sqrt(Cx**2 + Cy**2)
    if d > (L1 + L2) or d < abs(L1 - L2):
        return None, None
    cos_theta2 = (Cx**2 + Cy**2 - L1**2 - L2**2) / (2 * L1 * L2)
    theta2 = math.acos(cos_theta2)
    k1, k2 = L1 + L2 * math.cos(theta2), L2 * math.sin(theta2)
    theta1 = math.atan2(Cy, Cx) - math.atan2(k2, k1)
    return math.degrees(theta1), math.degrees(theta2)

# Map potentiometer value to coordinates
def map_potentiometer_to_coordinates(value, min_val, max_val, min_coord, max_coord):
    return min_coord + (value - min_val) * (max_coord - min_coord) / (max_val - min_val)

# Main loop
def main():
    try:
        # Initialize servos
        servo_shoulder = PWM(Pin(0))
        servo_elbow = PWM(Pin(1))
        servo_shoulder.freq(50)
        servo_elbow.freq(50)

        # Initialize potentiometers
        x_pot = ADC(Pin(26))
        y_pot = ADC(Pin(27))

        # Calibration and workspace boundaries
        pot_min, pot_max = 0, 65535
        x_min, x_max, y_min, y_max = -150, 150, 0, 200

        while True:
            # Read potentiometer values
            x_value = x_pot.read_u16()
            y_value = y_pot.read_u16()

            # Map potentiometer values to coordinates
            x_coord = map_potentiometer_to_coordinates(x_value, pot_min, pot_max, x_min, x_max)
            y_coord = map_potentiometer_to_coordinates(y_value, pot_min, pot_max, y_min, y_max)

            # Clamp coordinates
            x_coord = max(x_min, min(x_max, x_coord))
            y_coord = max(y_min, min(y_max, y_coord))

            print(f"Coordinates: X={x_coord:.2f}, Y={y_coord:.2f}")

            # Compute inverse kinematics
            angles = calculate_inverse_kinematics(x_coord, y_coord)
            if angles == (None, None):
                print("Unreachable point")
                continue

            shoulder_angle, elbow_angle = angles
            print(f"Target angles: Shoulder={shoulder_angle:.2f}°, Elbow={elbow_angle:.2f}°")

            # Move servos to calculated angles
            move_servo(servo_shoulder, shoulder_angle)
            move_servo(servo_elbow, elbow_angle)

            # Read feedback from ADS1015
            feedback_shoulder = adc.read(0, ADS1015_A_FB)
            feedback_elbow = adc.read(0, ADS1015_B_FB)
            print(f"Servo Feedback: Shoulder={feedback_shoulder}, Elbow={feedback_elbow}")

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()
