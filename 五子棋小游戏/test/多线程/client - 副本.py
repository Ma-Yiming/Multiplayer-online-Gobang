import socket
import threading
import time

class Client():
    def __init__(self,ip_port):
        self.num = ''
        self.iswaiting=0
        self.sk = socket.socket()
        self.sk.connect(ip_port)
        self.sk.settimeout(5)
        self.name = input('你的名字：')+'：'
        self.thread()
    def wait(self):
        while True:
            try:
                data = self.sk.recv(1024).decode()
                print(data)
                if self.num == '':
                    self.num=((data.split('|')[1])[0])
                break
            except:
                continue
    def round(self):
        self.wait()
        if self.num == '1':
            while True:
                self.iswaiting=0
                send_data=self.name+input('>>')
                self.sk.sendall(bytes(self.num+':'+send_data,encoding='utf-8'))
                self.iswaiting=1
                self.wait()
        elif self.num == '2':
            while True:
                self.iswaiting=1
                self.wait()
                self.iswaiting=0
                send_data=self.name+input('>>')
                self.sk.sendall(bytes(self.num+':'+send_data,encoding='utf-8'))
    def thread(self):
        t = threading.Thread(target=self.round)
        t.start()
        while True:
            if self.iswaiting:
                time.sleep(1)
                print(111111)

a=Client(('127.0.0.1',8002))
