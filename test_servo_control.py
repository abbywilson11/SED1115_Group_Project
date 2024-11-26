# GP 0 is shoulder
# GP 1 is elbow 
# GP 2 is pen

# left knob controls elbow 
# right knob will control shoulder

from servo_control import *
import time

def test_initialize_servo():
    print("Testing Servo Initialization...")
    servo = initialize_servo(1)  # Replace with the correct GPIO pin
    if servo:
        print("Servo initialization passed.")
    else:
        print("Servo initialization failed.")

def test_translate():
    print("Testing Angle-to-Duty Cycle Translation...")
    for angle in [-10, 0, 45, 90, 135, 180, 200]:
        duty = translate(angle)
        print(f"Angle: {angle}, Duty Cycle: {duty}")

def test_move_servo():
    print("Testing Servo Movement...")
    servo = initialize_servo(1)
    if not servo:
        print("Servo not initialized, skipping move tests.")
        return
    for angle in [0, 90, 180, -15, 200]:
        move_servo_to_angle(servo, angle)

def test_check_servo_usage():
    print("Testing Continuous Usage and Overheating Warning...")
    servo = initialize_servo(1)
    if not servo:
        print("Servo not initialized, skipping usage tests.")
        return
    start_time = time.time()
    for i in range(0, 180, 30):
        move_servo_to_angle(servo, i)
        check_servo_usage(start_time)
        time.sleep(0.5)

if __name__ == "__main__":
    test_initialize_servo()
    test_translate()
    test_move_servo()
    test_check_servo_usage()