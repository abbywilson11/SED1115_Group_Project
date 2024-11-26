'''from servo_control import initialize_servo, move_servo_to_angle, translate, check_servo_usage
import time

def test_initialize_servo():
    print("Testing Servo Initialization...")
    servo = initialize_servo(15)  # Replace with the correct GPIO pin
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
    servo = initialize_servo(15)
    if not servo:
        print("Servo not initialized, skipping move tests.")
        return
    for angle in [0, 90, 180, -15, 200]:
        move_servo_to_angle(servo, angle)

def test_check_servo_usage():
    print("Testing Continuous Usage and Overheating Warning...")
    servo = initialize_servo(15)
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
    test_check_servo_usage()'''

# Import necessary modules
from machine import Pin, PWM, ADC
import time

# Import functions from your servo code
# Replace 'servo_control' with the actual name of your Python file (without .py)
from servo_control import initialize_servo, translate, move_servo_to_angle, read_and_convert_knob_values

# Test Function Definitions
def test_translate():
    """Test angle-to-duty cycle translation."""
    print("Testing translate function...")
    assert translate(0) == 2300, "Failed: 0° should translate to 2300 duty cycle"
    assert translate(180) == 7500, "Failed: 180° should translate to 7500 duty cycle"
    assert 4000 <= translate(90) <= 5000, "Failed: 90° should be within a valid duty cycle range"
    print("translate function passed all tests!")

def test_potentiometer_to_angle():
    """Test potentiometer inputs and angle conversion."""
    print("Testing potentiometer to angle conversion...")
    
    # Simulate reading ADC values
    x_pin = 26  # Replace with actual x-axis pin
    y_pin = 27  # Replace with actual y-axis pin
    
    adc_x = ADC(Pin(x_pin))
    adc_y = ADC(Pin(y_pin))
    
    # Read ADC values
    x_value = adc_x.read_u16()
    y_value = adc_y.read_u16()
    
    # Convert ADC to angles
    x_angle = int(x_value / 65535 * 180)
    y_angle = int(y_value / 65535 * 180)
    
    assert 0 <= x_angle <= 180, "Failed: x_angle out of range"
    assert 0 <= y_angle <= 180, "Failed: y_angle out of range"
    print(f"Potentiometer readings converted: x_angle={x_angle}, y_angle={y_angle}")
    print("Potentiometer to angle conversion passed!")

def test_servo_movement():
    """Test servo movements for boundary and mid-range angles."""
    print("Testing servo movements...")
    
    # Initialize servos
    shoulder_servo = initialize_servo(0)  # Replace 0 with the GPIO pin for shoulder servo
    elbow_servo = initialize_servo(1)    # Replace 1 with the GPIO pin for elbow servo
    pen_servo = initialize_servo(2)      # Replace 2 with the GPIO pin for pen servo

    # Test each servo
    for servo in [shoulder_servo, elbow_servo, pen_servo]:
        move_servo_to_angle(servo, 0)  # Move to 0°
        time.sleep(1)  # Small delay to observe movement
        move_servo_to_angle(servo, 90)  # Move to 90°
        time.sleep(1)
        move_servo_to_angle(servo, 180)  # Move to 180°
        time.sleep(1)
    
    print("Servo movement tests passed!")

def test_potentiometer_servo_integration():
    """Test integration of potentiometer input with servo control."""
    print("Testing potentiometer-servo integration...")
    
    # Initialize servos
    shoulder_servo = initialize_servo(0)  # Replace 0 with the GPIO pin for shoulder servo
    elbow_servo = initialize_servo(1)    # Replace 1 with the GPIO pin for elbow servo
    pen_servo = initialize_servo(2)      # Replace 2 with the GPIO pin for pen servo
    
    # Potentiometer pins
    x_pin = 26
    y_pin = 27
    
    # Simulate a loop to test servo control based on potentiometer
    for _ in range(5):  # Adjust loop count as needed
        # Read potentiometer values
        x_angle, y_angle = read_and_convert_knob_values(x_pin, y_pin)
        
        # Move servos based on angles
        move_servo_to_angle(shoulder_servo, x_angle)
        move_servo_to_angle(elbow_servo, y_angle)
        move_servo_to_angle(pen_servo, (x_angle + y_angle) // 2)  # Example pen servo behavior
        
        time.sleep(1)  # Observe movement

    print("Potentiometer-servo integration test passed!")

# Run All Tests
if __name__ == "__main__":
    print("Starting tests...")
    test_translate()
    while True:
        test_potentiometer_to_angle()
        time.sleep(1)

test_servo_movement()
    #test_potentiometer_servo_integration()
print("All tests completed successfully!")