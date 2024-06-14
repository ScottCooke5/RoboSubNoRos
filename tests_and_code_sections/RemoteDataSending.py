import socket
import pygame
import time

def send_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode('utf-8'))
        response = s.recv(1024)
        print(f'Received: {response.decode("utf-8")}')

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()
    
    # Ensure at least one joystick is connected
    if pygame.joystick.get_count() == 0:
        print("No joystick connected!")
        exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    host = '192.168.1.2'  # Replace with the Jetson's IP address
    port = 65432

    try:
        while True:
            pygame.event.pump()
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
            #data = axes
            data = f"{axes},{buttons}"
            #print(axes, buttons)
            send_data(host, port, data)
            time.sleep(.1)  # Send data at a reasonable rate
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()