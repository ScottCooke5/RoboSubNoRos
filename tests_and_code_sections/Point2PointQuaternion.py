import numpy as np
import quaternion

def vector_to_quaternion_rotation(initial_vector, target_vector):
    # Normalize both vectors to ensure they are unit vectors
    initial_vector = initial_vector / np.linalg.norm(initial_vector)
    target_vector = target_vector / np.linalg.norm(target_vector)

    # Calculate the cross product and the angle between the vectors
    cross_prod = np.cross(initial_vector, target_vector)
    dot_prod = np.dot(initial_vector, target_vector)

    # Calculate the angle for the quaternion
    angle = np.arccos(dot_prod)

    # If vectors are opposite, handle the case of undefined rotation axis
    if np.isclose(angle, np.pi):
        # Find a perpendicular vector for the rotation axis (special case)
        axis = np.cross(initial_vector, np.array([1, 0, 0]))
        if np.linalg.norm(axis) < 1e-8:  # if initial vector is parallel to [1, 0, 0]
            axis = np.cross(initial_vector, np.array([0, 1, 0]))
        axis = axis / np.linalg.norm(axis)
    else:
        # Normalize the axis
        axis = cross_prod / np.linalg.norm(cross_prod)

    # Create the rotation quaternion
    rotation_quaternion = quaternion.from_rotation_vector(axis * angle)
    return rotation_quaternion

# Example usage:
initial_vector = np.array([1, 0, 0])  # Initial direction
target_vector = np.array([0, 1, 0])   # Target direction

# Get the rotation quaternion
rot_quaternion = vector_to_quaternion_rotation(initial_vector, target_vector)
print("Rotation Quaternion:", rot_quaternion)
