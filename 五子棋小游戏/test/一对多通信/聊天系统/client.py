import socket

class Client():
    def __init__(self,ip_port):
        self.num = ''
        self.sk = socket.socket()
        self.sk.connect(ip_port)
        self.sk.settimeout(5)
        self.name = input('你的名字：')+'：'
        self.round()
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
                send_data=self.name+input('>>')
                self.sk.sendall(bytes(self.num+':'+send_data,encoding='utf-8'))
                self.wait()
        elif self.num == '2':
            while True:
                self.wait()
                send_data=self.name+input('>>')
                self.sk.sendall(bytes(self.num+':'+send_data,encoding='utf-8'))

a=Client(('10.5.133.205',8002))
