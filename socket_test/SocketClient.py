#!/usr/bin/env python3

import socket

HOST = '192.168.1.200'  # 服务器的主机名或者 IP 地址
PORT = 8899        # 服务器使用的端口

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))