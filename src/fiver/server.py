import os
import time
import platform
import signal
import pickledb
import socket
import threading
from .utils import path_fiverdb, is_lunix
import psutil
import json

if is_lunix():
    import daemon

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

            t_receive_messages = threading.Thread(target=self.receive_messages)
            t_receive_messages.start()   
            t_send_information = threading.Thread(target=self.send_information)
            t_send_information.start()           

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

    def get_disk_info(self):
        disk_info = []
        
        # Iterate over all disk partitions
        for partition in psutil.disk_partitions():
            try:
                # Get disk usage statistics for each partition
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Append the partition information
                disk_info.append({
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'total': usage.total / (1024 ** 3),  # Convert bytes to GB
                    'used': usage.used / (1024 ** 3),    # Convert bytes to GB
                    'free': usage.free / (1024 ** 3),    # Convert bytes to GB
                    'percent_used': usage.percent
                })
           
            except:
                pass
        
        return disk_info

    def get_information(self):
        kernel = platform.release()
        if not kernel:
            kernel = platform.version()

        virtual_memory = psutil.virtual_memory()
        net_io = psutil.net_io_counters()

        return {"information_data": {
            "system": platform.system(),
            "node": platform.node(),
            "cpu":platform.processor(),
            "kernel": kernel,
            "architecture": platform.machine(),
            "num_logical_cores": psutil.cpu_count(),
            "num_physical_cores": psutil.cpu_count(logical=False),
            "total_memory": f"{virtual_memory.total / (1024 ** 3):.2f} GB",
            "available_memory": f"{virtual_memory.available / (1024 ** 3):.2f} GB",
            "used_memory": f"{virtual_memory.used / (1024 ** 3):.2f} GB",
            "percent_used_menory": f"{virtual_memory.used / virtual_memory.total * 100}",
            "net_stats": psutil.net_if_stats(),
            "bytes_sent" : f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
            "bytes_received": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB",
            "disk_info": self.get_disk_info(),
        }}

    def send_information(self):
        while True:
            try:
                self.connectionSocket.send(json.dumps(self.get_information()).encode())
                time.sleep(1)
            except:
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
            StartServer(serverIP, serverPort)
        case 'start':
            print(f"[server] Server is running at {serverIP}:{serverPort}")
            if is_lunix():
                with daemon.DaemonContext():
                    StartServer(serverIP, serverPort)
            else:
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
