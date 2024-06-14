import socket

# Define the server's IPv4 address and port
server_ipv6 = '192.168.1.2'      # Replace with the server's IPv4 address
server_port = 65432       # Replace with the port the server is listening on

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ipv6, server_port))

# Send data to the server
message = "Hello, Server!"
client_socket.sendall(message.encode())

# Close the connection
client_socket.close()