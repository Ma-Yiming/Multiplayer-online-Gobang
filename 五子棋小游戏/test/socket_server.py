import subprocess
import socket

ip_port=('127.0.0.1',9999)

s=socket.socket()
s.bind(ip_port)
s.listen(5)

while True:
    conn,add=s.accept()
    conn.sendall(bytes('欢迎致电 10086，请输入1***,0转人工服务',encoding='utf-8'))
    while True:
        try:
            recv_data = conn.recv(1024)
            if len(recv_data) == 0:
                break
            p=subprocess.Popen(str(recv_data,encoding='utf-8'),shell=True,\
                               stdout=subprocess.PIPE)
            res = p.stdout.read()
            if len(res) == 0:
                send_data = 'cmd err'
            else:
                send_data = str(res,econding='gbk')
            print(send_data)
            
            send_data = bytes(send_data,encoding='utf-8')

            ready_tag='Ready|%s' %len(send_data)
            conn.send(bytes(ready_tag,encoding='utf-8'))
            feedback=conn.recv(1024)
            feedback=str(feedback,encoding='utf-8')

            if feedback.startswith('Start'):
                conn.send(send_data)
        except Exception:
            break
    conn.close()
