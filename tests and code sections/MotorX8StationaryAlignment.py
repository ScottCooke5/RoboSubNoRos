import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Define the coordinates for 8 sets of points (each set consists of two points)
coordinates = [
    ([1, 1], [1, 1], [0, 1]), #front left up
    ([1, 1], [-1, -1], [0, 1]), #front right up
    ([-1, -1], [1, 1], [0, 1]), #back left up
    ([-1, -1], [-1, -1], [0, 1]), #back right up
    ([2, 2.707], [1, .293], [0, 0]), #front left diagonal
    ([2, 2.707], [-1, -.293], [0, 0]), #front right diagonal
    ([-2, -2.707], [1, .293], [0, 0]), #back left diagonal
    ([-2, -2.707], [-1, -.293], [0, 0]), #back right diagonal
    ([0, 1], [0, 0], [0, 0])  #sub direction facing
]

# Plot each set of points and a line connecting them
colors = plt.cm.jet(np.linspace(0, 1, len(coordinates)))  # Using a color map for variety
for (x, y, z), color in zip(coordinates, colors):
    ax.scatter(x, y, z, color=color, marker='o')  # All points are circles
    ax.plot(x, y, z, color=color)                 # Lines in the same color as points

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
