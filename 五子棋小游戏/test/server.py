#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket

ip_port = ('127.0.0.1',8888)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    conn,address =  sk.accept()
    conn.sendall(bytes('欢迎致电 10086，请输入1xxx,0转人工服务.',encoding='utf-8'))
    while True:
        try:
            data = conn.recv(1024).decode()
            print(data)
        except:
            break
        if data == 'q':
            break
        elif data == '0':
            conn.sendall(bytes('通过可能会被录音.balabala一大推',encoding='utf-8'))
        else:
            conn.sendall(bytes('请重新输入.',encoding='utf-8'))
    conn.close()
