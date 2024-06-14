import numpy as np
import quaternion  # This imports the quaternion extension


#--------------------------------------------------------------------------------------------------------------------------------
# Big function made by chatgpt to assign motor values
#--------------------------------------------------------------------------------------------------------------------------------

def motor_forces(current_orientation_q, desired_orientation_q, direction_vector):
    # Define the distances from the center to each type of motor
    r_d = 1.5  # Distance to diagonal motors
    r_v = 1.0  # Distance to vertical motors
    F = 1  # Unit force produced by each motor for simplicity
    
    # Control matrix A, considering different lever arms for torque calculation
    #      FrontL        FrontR          BackL          BackR   FLU FRU BLU BRU
    A = np.array([
        [F/np.sqrt(2), F/np.sqrt(2), -F/np.sqrt(2), -F/np.sqrt(2), 0, 0, 0, 0],  # Fx
        [-F/np.sqrt(2), F/np.sqrt(2), -F/np.sqrt(2), F/np.sqrt(2), 0, 0, 0, 0],  # Fy
        [0, 0, 0, 0, F, F, F, F],  # Fz
        [0, 0, 0, 0, r_v*F, -r_v*F, r_v*F, -r_v*F],  # T_x (Roll)
        [0, 0, 0, 0, -r_v*F, -r_v*F, r_v*F, r_v*F],   # T_y (Pitch, corrected)
        [-r_d*F, r_d*F, r_d*F, -r_d*F, 0, 0, 0, 0]  # T_z (Yaw)
    ])

    # Convert input quaternions from arrays to quaternion objects
    current_rotation = quaternion.quaternion(*current_orientation_q)
    desired_rotation = quaternion.quaternion(*desired_orientation_q)

    # Calculate the error rotation needed to achieve the desired orientation
    error_rotation = desired_rotation * current_rotation.inverse()

    # Convert the error quaternion to a numpy array to extract components
    error_quat = quaternion.as_float_array(error_rotation)

    # Calculate desired force direction in the current orientation frame
    transformed_direction_vector = quaternion.rotate_vectors(current_rotation, direction_vector)

    # Desired forces (Fx, Fy, Fz) and torques (Tx, Ty, Tz)
    k = 10  # Control gain for torques
    desired_forces_torques = np.array([
        transformed_direction_vector[0],  # Desired Fx
        transformed_direction_vector[1],  # Desired Fy
        transformed_direction_vector[2],  # Desired Fz
        k * error_quat[1],  # Proportional control for Tx (ignore scalar part)
        k * error_quat[2],  # Proportional control for Ty
        k * error_quat[3]   # Proportional control for Tz
    ])

    # Solve for motor forces using least squares
    motor_forces = np.linalg.lstsq(A, desired_forces_torques, rcond=None)[0]

    return motor_forces

#--------------------------------------------------------------------------------------------------------------------------------

def scale_forces(input, scale):
    max_value = max(map(abs, input))
    if max_value != 0:
        scaled = input * scale / max_value
    return scaled

#--------------------------------------------------------------------------------------------------------------------------------

def English2Quaternion(English):
    angle = np.radians(English[0]/2)
    axis = [English[1], English[2], English[3]]
    norm = np.linalg.norm(axis)
    if norm != 0:
        axis = axis / norm  # Can't normalize a zero vector, return original
    Q = [np.cos(angle), np.sin(angle)*axis[0], np.sin(angle)*axis[1], np.sin(angle)*axis[2]]
    return Q

#--------------------------------------------------------------------------------------------------------------------------------
# Testing the function
#--------------------------------------------------------------------------------------------------------------------------------

# Current orientation quaternion (0 degrees about z axis)
current_q = English2Quaternion([0, 0, 0, 1]) #degrees, axis

# Desired orientation quaternion (90 degrees about x axis)
desired_q = English2Quaternion([90, 1, 0, 0]) #degrees, axis

# Direction vector (move along global X)
direction_vector = [1, 0, 0]

# Call the function to compute motor forces
forces = motor_forces(current_q, desired_q, direction_vector)
forces_scaled = scale_forces(forces, 1)

# Print the motor forces
print("Motor forces:", forces_scaled)