import socket

def send_data(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode('utf-8'))
            data = s.recv(1024)
            print(f'Received: {data.decode("utf-8")}')

if __name__ == "__main__":
    host = '192.168.1.2'  # Replace with the Jetson's IP address
    port = 65432
    send_data(host, port)
