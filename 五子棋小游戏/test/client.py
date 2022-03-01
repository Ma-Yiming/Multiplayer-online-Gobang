#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
ip_port = ('127.0.0.1',8888)
sk = socket.socket()
try:
    sk.connect(ip_port)
    sk.settimeout(5)
    while True:
        try:
            data = sk.recv(1024).decode()
            print('receive:',data)
        except:
            print('服务器异常1......')
            break
        inp = input('please input:')
        sk.sendall(bytes(inp,encoding='utf-8'))
        if inp == 'q':
            break
    sk.close()
except:
    print('服务器异常2......')
    sk.close()
    

