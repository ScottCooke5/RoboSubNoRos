import numpy as np
import quaternion  # Adds support for quaternions to numpy

def rotate_point(point, axis, angle_degrees):
    # Convert the angle from degrees to radians
    angle = np.radians(angle_degrees)

    # Normalize the axis of rotation
    axis = axis / np.linalg.norm(axis)

    # Create the rotation quaternion
    q = quaternion.from_rotation_vector(angle * axis)

    # Convert the point to a quaternion
    p = np.quaternion(0, *point)

    # Compute the rotated point as a quaternion
    p_rotated = q * p * q.inverse()

    # Return the vector part of the quaternion
    return quaternion.as_float_array(p_rotated)[1:]

# Example usage:
point = np.array([1, 0, 0])
axis = np.array([0, 1, 0])  # Rotate around the y-axis
angle_degrees = 90  # Rotate 90 degrees

rotated_point = rotate_point(point, axis, angle_degrees)
print("Original point:", point)
print("Rotated point:", rotated_point)
