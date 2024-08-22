# import os
# import platform

# print(os.name)
# print(platform.machine())


import socket
import time
serverIP = "127.0.0.10"
serverPort = 10000
maxBytes = 4096


data = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, serverPort))
while True:
    data += 1
    time.sleep(1)
    print(data)
    sock.send(str(data).encode())
    modifiedMessage = sock.recv(maxBytes)

    modifiedMessage = modifiedMessage.decode()
    print(modifiedMessage)