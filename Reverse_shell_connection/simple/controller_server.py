import socket

CMD = b'echo "Just Hacked you!" >> payload.txt'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# carryout port binding
server_socket.bind(('127.0.0.1', 9000))

# listen for incoming connection
server_socket.listen()
print('[+} Controller is listening for incoming connections...')

try:

    # This blocks until a connection is received
    connection, address = server_socket.accept()
    print(f"[+] Connected to {address}")

    # We send the command to the target
    connection.sendall(CMD)
    print(f"[+] Send payload to {address}")

finally:

    # clean up th connection
    if 'connection' in locals():
        connection.close()
    server_socket.close()