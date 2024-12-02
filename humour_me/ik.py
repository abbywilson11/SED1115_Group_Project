import math

L1, L2 = 155, 155  # Lengths of the arm segments

def calculate_inverse_kinematics(x, y):
    """
    Calculate the angles (alpha, beta) using inverse kinematics.
    """
    # Calculate the distance from the base to the target point
    distance = math.sqrt(x**2 + y**2)

    if distance > (L1 + L2) or distance < abs(L1 - L2):
        print("Target is out of reach.")
        return None, None

    # Calculate angles using trigonometry
    cos_angle_a = (L1**2 + distance**2 - L2**2) / (2 * L1 * distance)
    angle_a = math.acos(cos_angle_a)

    cos_angle_b = (L1**2 + L2**2 - distance**2) / (2 * L1 * L2)
    angle_b = math.acos(cos_angle_b)

    # Convert to degrees
    alpha = math.degrees(angle_a + math.atan2(y, x))
    beta = math.degrees(angle_b)

    return alpha, beta

if __name__ == "__main__":
    alpha, beta = calculate_inverse_kinematics(100, 100)
    print(f"Alpha: {alpha}, Beta: {beta}")
