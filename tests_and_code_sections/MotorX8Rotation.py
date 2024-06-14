import numpy as np
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#--------------------------------------------------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------------------------------

def rotate_point(p, q):
    # Convert the point to a quaternion
    p = np.quaternion(0, *p)

    # Compute the rotated point as a quaternion
    p_rotated = q * p * q.inverse()

    # Return the vector part of the quaternion
    return quaternion.as_float_array(p_rotated)[1:]

#--------------------------------------------------------------------------------------------------------------------------------

def get_vector_from_user():
    while True:
        try:
            x = float(input("Enter the x component of the vector: "))
            y = float(input("Enter the y component of the vector: "))
            z = float(input("Enter the z component of the vector: "))
            return np.array([x, y, z])
        except ValueError:
            print("Please enter valid floating-point numbers.")

#--------------------------------------------------------------------------------------------------------------------------------

def rotate_sub(start_coordinates, q):
    '''
    end_coordinates = [
        ([0, 0, 0], [0, 0, 0]), #front left up
        ([0, 0, 0], [0, 0, 0]), #front right up
        ([0, 0, 0], [0, 0, 0]), #back left up
        ([0, 0, 0], [0, 0, 0]), #back right up
        ([0, 0, 0], [0, 0, 0]), #front left diagonal
        ([0, 0, 0], [0, 0, 0]), #front right diagonal
        ([0, 0, 0], [0, 0, 0]), #back left diagonal
        ([0, 0, 0], [0, 0, 0]), #back right diagonal
        ([0, 0, 0], [1, 0, 0])  #sub direction facing
    ]
    '''
    end_coordinates = []

    i = 0
    while i <= 8:
        end_coordinates.append((rotate_point(start_coordinates[i][0], q), rotate_point(start_coordinates[i][1], q)))
        i += 1

    print(end_coordinates)
    return end_coordinates

#--------------------------------------------------------------------------------------------------------------------------------
# Initial Sub Display / Initial Vectors
#--------------------------------------------------------------------------------------------------------------------------------


# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Define the coordinates for 8 sets of points (each set consists of two points)
coordinates = [
    ([1, 1, 0], [1, 1, 1]), #front left up
    ([1, -1, 0], [1, -1, 1]), #front right up
    ([-1, 1, 0], [-1, 1, 1]), #back left up
    ([-1, -1, 0], [-1, -1, 1]), #back right up
    ([2, 1, 0], [2.707, .293, 0]), #front left diagonal
    ([2, -1, 0], [2.707, -.293, 0]), #front right diagonal
    ([-2, 1, 0], [-2.707, .293, 0]), #back left diagonal
    ([-2, -1, 0], [-2.707, -.293, 0]), #back right diagonal
    ([0, 0, 0], [1, 0, 0])  #sub direction facing
]

# Plot each line
for line in coordinates:
    point1, point2 = line
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    z_values = [point1[2], point2[2]]
    ax.plot(x_values, y_values, z_values)

# Set the axes limits
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])

# Set labels for axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set the title
ax.set_title('3D Multiple Lines Plot')

# Show the plot
plt.show()

#--------------------------------------------------------------------------------------------------------------------------------
# Ask for new orientation <x, y, z> direction vector
#--------------------------------------------------------------------------------------------------------------------------------

user_vector = get_vector_from_user()
print("You entered the vector:", user_vector)
user_vector = user_vector / np.linalg.norm(user_vector) #normalized the user vector
#this is redundant right now because the vector to quaternion rotation fuction already normalizes, but it may be needed later
print(coordinates[0][0])

#--------------------------------------------------------------------------------------------------------------------------------
# Rotate sub based on vector
#--------------------------------------------------------------------------------------------------------------------------------

rot_quaternion = vector_to_quaternion_rotation(coordinates[8][1], user_vector)
print("Rotation Quaternion:", rot_quaternion)
coordinates = rotate_sub(coordinates, rot_quaternion)

#--------------------------------------------------------------------------------------------------------------------------------
# Display new sub
#--------------------------------------------------------------------------------------------------------------------------------

# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Plot each line
for line in coordinates:
    point1, point2 = line
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    z_values = [point1[2], point2[2]]
    ax.plot(x_values, y_values, z_values)

# Set the axes limits
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])

# Set labels for axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set the title
ax.set_title('3D Multiple Lines Plot')

# Show the plot
plt.show()


'''
# Example usage:
point = np.array([1, 0, 0])
axis = np.array([0, 1, 0])  # Rotate around the y-axis
angle_degrees = 90  # Rotate 90 degrees

rotated_point = rotate_point(point, axis, angle_degrees)
print("Original point:", point)
print("Rotated point:", rotated_point)

#--------------------------------------------------------------------------------------------------------------------------------

# Example usage:
initial_vector = np.array([1, 0, 0])  # Initial direction
target_vector = np.array([0, 1, 0])   # Target direction

# Get the rotation quaternion
rot_quaternion = vector_to_quaternion_rotation(initial_vector, target_vector)
print("Rotation Quaternion:", rot_quaternion)
'''
