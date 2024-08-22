import daemon
import os
import signal
import pickledb
import socket
import threading
from .utils import path_fiverdb


def check_status():
    db = pickledb.load(path_fiverdb(), False)
    pid = db.get('pid')
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
        
class StartServer:
    def __init__(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.connectionSocket = None
        self.save_pid()
        self.create_socket()

    def save_pid(self):
        pid = os.getpid()
        db = pickledb.load(path_fiverdb(), False)
        db.set('pid', pid)
        db.dump()

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.serverIP, self.serverPort))
        sock.listen()
        while True:
            connectionSocket, address = sock.accept()         
            print("[server] TCP connection address:", address)

            self.connectionSocket = connectionSocket

            t = threading.Thread(target=self.receive_messages)
            t.start()       
        
    def receive_messages(self):
        maxBytes = 4096
        while True:
            try:
                message = self.connectionSocket.recv(maxBytes)

                if not message: 
                    break
                message = message.decode()
                modifiedMessage = message.upper()
                # print(message)
                self.connectionSocket.send(modifiedMessage.encode())
            except:
               break

           
        self.connectionSocket.close()
        print('[server] Close socket')
  

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
            StartServer(serverIP, serverPort)
        case 'start':
            print(f"[server] Server is running at {serverIP}:{serverPort}")
            with daemon.DaemonContext():
                StartServer(serverIP, serverPort)
        case 'status':
            if check_status():
                print("[status] Fiver is running")
            else:
                print("[status] Fiver stopped")
        case 'stop':
            stop_server()
        case _:
            check_status()
