import socket
import pickle
import pygame

def receive_data():
    server_address = '192.168.1.2'  # Replace with the Jetson's IP address
    server_port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen()

        print(f"Server listening on {server_address}:{server_port}")

        while True:
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            with connection:
                while True:
                    serialized_data = connection.recv(1024)
                    if not serialized_data:
                        break
                    try:
                        data = pickle.loads(serialized_data)
                        axes = data['axes']
                        buttons = data['buttons']
                        
                        # Example: Process the received data
                        # Note: Replace this with your specific processing logic
                        print(f"Axes: {axes}")
                        print(f"Buttons: {buttons}")

                        # Send a response back to the client
                        response = "Data received successfully"
                        connection.sendall(response.encode('utf-8'))
                    except pickle.UnpicklingError as e:
                        print(f"Error unpickling data: {e}")
                        connection.sendall("Error unpickling data".encode('utf-8'))

if __name__ == '__main__':
    receive_data()
