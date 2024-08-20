import daemon
import os
import signal
import pickledb
import socket
from .utils import path_fiverdb


def check_status():
    db = pickledb.load(path_fiverdb(), False)
    pid = db.get('pid')
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
        

def start_server(serverIP, serverPort):
    pid = os.getpid()

    db = pickledb.load(path_fiverdb(), False)
    db.set('pid', pid)
    db.dump()

    maxBytes = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((serverIP, serverPort))
    sock.listen()
    
    while True:
        connectionSocket, address = sock.accept()
        message = connectionSocket.recv(maxBytes)
        print("TCP connection address:", address)

        message = message.decode()
        modifiedMessage = message.upper()
        connectionSocket.send(modifiedMessage.encode())
        pass

def stop_server():
    db = pickledb.load(path_fiverdb(), False)
    pid = db.get('pid')

    if check_status():
        os.kill(pid, signal.SIGTERM)  # ctrl + C
        print("[stop] Server is stopped")

        # os.kill(pid, signal.SIGKILL)  # shutdown
    else:
        print("[stop] Server is not running")
    

def server_app(server_arg):
    # server_arg: ['debug', 'start', 'status', 'stop', ]
    serverIP = "127.0.0.10"
    serverPort = 10000

    match server_arg:
        case 'debug':
            print(f"[server] Server is running at {serverIP}:{serverPort}")
            start_server(serverIP, serverPort)
        case 'start':
            print(f"[server] Server is running at {serverIP}:{serverPort}")
            with daemon.DaemonContext():
                start_server(serverIP, serverPort)
        case 'status':
            if check_status():
                print("[status] Fiver is running")
            else:
                print("[status] Fiver stopped")
        case 'stop':
            stop_server()
        case _:
            check_status()
