import math

# Link lengths (in mm)
L_a = 100  # Length of the first link
L_b = 100  # Length of the second link

def calculate_inverse_kinematics(Ax, Ay, Cx, Cy):
    """
    Calculate the joint angles (alpha and beta) using the lab's provided equations.
    Inputs:
    - Ax, Ay: Coordinates of the base point (point A)
    - Cx, Cy: Target coordinates for the end effector (point C)
    Outputs:
    - servoA_angle: Angle for servo A in degrees
    - servoB_angle: Angle for servo B in degrees
    """
    # Step 1: Calculate distances
    AC = math.sqrt((Ax - Cx)**2 + (Ay - Cy)**2)
    A_baseC = math.sqrt((Ax - Cx)**2 + Cy**2)
    
    # Step 2: Calculate intermediate angles
    BAC = math.acos((L_a**2 + AC**2 - L_b**2) / (2 * L_a * AC))
    ACB = math.asin((L_a * math.sin(BAC)) / L_b)
    Y_AC = math.acos((Ay * AC + A_baseC**2) / (2 * Ay * AC))
    
    # Step 3: Calculate angles
    alpha = math.degrees(BAC + Y_AC)  # Shoulder angle
    beta = math.degrees(BAC + ACB)   # Elbow angle
    
    # Step 4: Servo-specific calculations
    servoA_angle = alpha - 75
    servoB_angle = 150 - beta

    return servoA_angle, servoB_angle
