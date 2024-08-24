# import os
# import platform

# print(os.name)
# print(platform.machine())


import socket
import time
import json
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
    # sock.send(str(data).encode())
    modifiedMessage = sock.recv(maxBytes)
    
    modifiedMessage = json.loads(modifiedMessage.decode())
    print(modifiedMessage["system"])


# import psutil

# # CPU usage percentage
# cpu_usage = psutil.cpu_percent(interval=1)
# print(f"CPU Usage: {cpu_usage}%")

# num_logical_cores = psutil.cpu_count()
# print(f"Logical Cores: {num_logical_cores}")

# # Number of physical CPU cores
# num_physical_cores = psutil.cpu_count(logical=False)
# print(f"Physical Cores: {num_physical_cores}")


# # Virtual memory usage
# virtual_memory = psutil.virtual_memory()
# print(f"Total Memory: {virtual_memory.total / (1024 ** 3):.2f} GB")
# print(f"Available Memory: {virtual_memory.available / (1024 ** 3):.2f} GB")
# print(f"Used Memory: {virtual_memory.used / (1024 ** 3):.2f} GB")

# # Swap memory usage
# swap_memory = psutil.swap_memory()
# print(f"Total Swap: {swap_memory.total / (1024 ** 3):.2f} GB")
# print(f"Used Swap: {swap_memory.used / (1024 ** 3):.2f} GB")

# # Disk usage for the root partition
# disk_usage = psutil.disk_usage('F:/')
# print(f"Total Disk Space: {disk_usage.total / (1024 ** 3):.2f} GB")
# print(f"Used Disk Space: {disk_usage.used / (1024 ** 3):.2f} GB")
# print(f"Free Disk Space: {disk_usage.free / (1024 ** 3):.2f} GB")

# # Disk partitions
# partitions = psutil.disk_partitions()
# for partition in partitions:
#     print(f"Device: {partition.device}")
#     print(f"Mount Point: {partition.mountpoint}")
#     print(f"File System Type: {partition.fstype}")

# # Network statistics
# net_stats = psutil.net_if_stats()
# for interface, stats in net_stats.items():
#     print(f"Interface: {interface}")
#     print(f"Is Up: {stats.isup}")
#     print(f"Speed: {stats.speed} Mbps")

# # Network I/O statistics
# net_io = psutil.net_io_counters()
# print(f"Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB")
# print(f"Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")
