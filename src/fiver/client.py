import socket

def client_app(address):
    try:
        serverIP, serverPort = address.split(':')
    except:
        return print("[error] Ip server is incorrect")
 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((serverIP, int(serverPort)))
    except socket.error as e:
        return print(f"[error] {e}")
    

    maxBytes = 4096
    data = 'sss'
    sock.send(data.encode())
    modifiedMessage = sock.recv(maxBytes)
    sock.close()

    modifiedMessage = modifiedMessage.decode()
    print(modifiedMessage)