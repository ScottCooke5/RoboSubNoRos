import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Define the coordinates for 8 sets of points (each set consists of two points)
coordinates = [
    ([1, 4], [2, 5], [3, 6]),
    ([2, 3], [4, 1], [5, 7]),
    ([1, 0], [0, 1], [1, 3]),
    ([3, 7], [8, 2], [1, 5]),
    ([6, 5], [7, 9], [2, 8]),
    ([9, 8], [1, 3], [4, 6]),
    ([4, 6], [5, 3], [7, 9]),
    ([7, 2], [6, 1], [5, 3])
]

# Plot each set of points and a line connecting them
colors = plt.cm.jet(np.linspace(0, 1, len(coordinates)))  # Using a color map for variety
for (x, y, z), color in zip(coordinates, colors):
    ax.scatter(x, y, z, color=color, marker='o')  # All points are circles
    ax.plot(x, y, z, color=color)                 # Lines in the same color as points

# Set labels for axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set the title
ax.set_title('3D Multiple Lines Plot')

# Show the plot
plt.show()
