import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Arm length constants
L1, L2 = 155, 155

# Forward Kinematics Function
def forward_kinematics(theta1, theta2):
    """Calculate the position of the end effector (x, y) using forward kinematics."""
    x = L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2)
    y = L1 * math.sin(theta1) + L2 * math.sin(theta1 + theta2)
    return x, y

# Plotting Function
def plot_forward_kinematics(theta1, theta2):
    """Plot the robotic arm for the given theta1 and theta2 angles."""
    ax.clear()
    
    # Calculate end-effector position using forward kinematics
    x, y = forward_kinematics(theta1, theta2)
    
    # Joint positions
    x0, y0 = 0, 0
    x1, y1 = L1 * np.cos(theta1), L1 * np.sin(theta1)
    
    # Plot arm links
    ax.plot([x0, x1, x], [y0, y1, y], 'o-', markersize=10, lw=3, label='Arm Links')
    ax.scatter(x, y, c='red', s=100, label="End Effector")
    
    # Plot the joint angles
    ax.text(x1 / 2, y1 / 2, f"θ₁ = {np.degrees(theta1):.1f}°", fontsize=10, color='blue')
    ax.text((x1 + x) / 2, (y1 + y) / 2, f"θ₂ = {np.degrees(theta2):.1f}°", fontsize=10, color='green')
    
    # Plot details
    ax.set_xlim(-L1 - L2 - 10, L1 + L2 + 10)
    ax.set_ylim(-L1 - L2 - 10, L1 + L2 + 10)
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    ax.set_title("2-Link Arm Forward Kinematics")
    ax.set_xlabel("X-axis (mm)")
    ax.set_ylabel("Y-axis (mm)")
    ax.legend()
    
    plt.draw()

# Slider Update Function
def update(val):
    """Update the plot based on slider values."""
    theta1 = np.radians(slider_theta1.val)
    theta2 = np.radians(slider_theta2.val)
    plot_forward_kinematics(theta1, theta2)

# Initial angles
theta1_init, theta2_init = 45, 30  # Initial angles in degrees
theta1_rad = np.radians(theta1_init)
theta2_rad = np.radians(theta2_init)

# Initial plot setup
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.3)
plot_forward_kinematics(theta1_rad, theta2_rad)

# Slider setup
ax_theta1 = plt.axes([0.2, 0.2, 0.65, 0.03])
ax_theta2 = plt.axes([0.2, 0.15, 0.65, 0.03])

slider_theta1 = Slider(ax_theta1, 'θ₁ (shoulder)', 0, 180, valinit=theta1_init)
slider_theta2 = Slider(ax_theta2, 'θ₂ (elbow)', 0, 180, valinit=theta2_init)

slider_theta1.on_changed(update)
slider_theta2.on_changed(update)

plt.show()