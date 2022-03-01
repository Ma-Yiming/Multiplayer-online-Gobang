import socket
import threading
import select

Player1='0'
Player2='0'
i=0
P1issent=0
P2issent=0
#初始1先发送
whosend=1
def process(request, client_address):
    #这五个变量是联系两个客户端的
    global i,Player1,Player2,P1issent,P2issent,whosend
    #每次进来一个客户就加一
    i+=1
    #i用来告诉服务端我是谁，this是函数内变量，用来告诉自己自己是谁
    this=i
    
    print(request,client_address)

    conn = request
    #第一次来的是1号，第二次是2号
    conn.sendall(bytes('欢迎|%d号玩家.'%i,encoding='utf-8'))
    flag = True
    #开始等待客户端发消息
    while flag:
        #接受消息:
        #轮流发送消息
        #轮到这个客户端发送
        print('this:',this,'whosend:',whosend,'P1issent:',P1issent\
              ,'P2issent:',P2issent)
        if whosend == this:
            data = conn.recv(1024).decode()
            #who是哪个客户，data是发送过来的消息
            who = int(data.split(':')[0])
            data = data.split(':')[1]
            print(who,data)
            #按理来说，1号客户先发送消息，此时2号在等待，1号发送之后2号接受
            #2号变为发送状态，1号变为接受状态
            if who==1:
                #将1号要发的消息存入Player1
                #发送给1号2号发来的消息
                Player1=data
                P1issent=1
            else:
                #将2号要发的消息存入Player1
                #发送给2号1号发来的消息
                Player2=data
                P2issent=1
        else:
            whowait = (whosend)%2+1
            if whowait == 1:
                while not P2issent:
                    pass
                conn.sendall(bytes(Player2,encoding='utf-8'))
                whosend=1
                P2issent=0
            else:
                while not P1issent:
                    pass
                conn.sendall(bytes(Player1,encoding='utf-8'))
                whosend=2
                P1issent=0
 
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(('10.5.133.205',8002))
sk.listen(5)
 
while True:
    r, w, e = select.select([sk,],[],[],1)
    
    if sk in r:
        print('get request')
        request, client_address = sk.accept()
        t = threading.Thread(target=process, args=(request, client_address))
        t.daemon = False
        t.start()
 
sk.close()
