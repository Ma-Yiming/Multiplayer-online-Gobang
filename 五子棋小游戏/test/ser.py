#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket

ip_port = ('192.168.43.23',8888)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    conn,address =  sk.accept()
    conn.sendall(bytes('欢迎使用聊天系统.',encoding='utf-8'))
    while True:
        try:
            data = conn.recv(1024).decode()
            print(data)
        except:
            #这里写break以为着我一直在等信号过来,写pass意味着不管信号来不来
            continue
        feedback = input(">>")
        conn.sendall(bytes("马艺鸣："+feedback,encoding='utf-8'))
    conn.close()
