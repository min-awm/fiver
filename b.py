import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))  # Connect to the server at localhost on port 9999
    
    while True:
        # Read command from user input
        command = input("Enter command to execute: ")
        if command.lower() == 'exit':
            break
        
        # Send the command to the server
        client_socket.sendall(command.encode('utf-8'))
        
        # Receive the response from the server
        response = client_socket.recv(4096).decode('utf-8')
        print(response)
    
    client_socket.close()

if __name__ == "__main__":
    main()
