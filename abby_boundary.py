import math
from machine import Pin, PWM
from time import sleep

# Servo motor control class
class Servo:
    def __init__(self, pin, min_pulse=500, max_pulse=2500, freq=50):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.angle = 0
        self.set_angle(90)  # Default to center (90 degrees)

    def set_angle(self, angle):
        if angle < 0 or angle > 180:
            raise ValueError("Angle out of bounds: 0-180 degrees allowed")
        self.angle = angle
        pulse_width = self.min_pulse + (self.max_pulse - self.min_pulse) * angle // 180
        self.pwm.duty_u16(int(pulse_width * 65535 // 20000))  # Normalize to 16-bit

# Inverse kinematics for a 2-link planar arm
class RoboticArm:
    def __init__(self, l1, l2):
        self.l1 = l1  # Length of link 1
        self.l2 = l2  # Length of link 2
        self.joint1 = Servo(0)  # Base
        self.joint2 = Servo(1)  # Elbow
        self.origin = (0, 0)  # Define origin in Cartesian coordinates
        self.boundaries = [
            (0, 180),  # Joint 1 boundaries
            (0, 180),  # Joint 2 boundaries
        ]

    def inverse_kinematics(self, x, y):
        # Calculate joint angles using trigonometry
        r = math.sqrt(x**2 + y**2)
        if r > (self.l1 + self.l2) or r < abs(self.l1 - self.l2):
            raise ValueError("Target out of reach")
        
        # Joint 2 angle
        cos_theta2 = (x**2 + y**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        theta2 = math.acos(cos_theta2)  # Elbow angle
        theta2_deg = math.degrees(theta2)

        # Joint 1 angle
        k1 = self.l1 + self.l2 * math.cos(theta2)
        k2 = self.l2 * math.sin(theta2)
        theta1 = math.atan2(y, x) - math.atan2(k2, k1)
        theta1_deg = math.degrees(theta1)

        return theta1_deg, theta2_deg

    def move_to(self, x, y):
        theta1, theta2 = self.inverse_kinematics(x, y)

        # Enforce boundaries
        if not (self.boundaries[0][0] <= theta1 <= self.boundaries[0][1]):
            raise ValueError(f"Joint 1 angle out of bounds: {theta1}")
        if not (self.boundaries[1][0] <= theta2 <= self.boundaries[1][1]):
            raise ValueError(f"Joint 2 angle out of bounds: {theta2}")

        # Move servos to calculated angles
        self.joint1.set_angle(theta1)
        self.joint2.set_angle(theta2)

    def go_to_origin(self):
        self.move_to(self.origin[0], self.origin[1])

# Main program
def main():
    arm = RoboticArm(l1=155, l2=155)  # Arm with two 100mm links
    arm.go_to_origin()  # Start at origin
    try:
        # Move to a specific point
        arm.move_to(50, 50)
        sleep(2)

        # Return to origin
        arm.go_to_origin()
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
