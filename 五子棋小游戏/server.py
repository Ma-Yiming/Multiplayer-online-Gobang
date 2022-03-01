import socket
import threading
import select

#初始化所有变量
Player1=['0','0']
Player2=['0','0']
i=0
P1issent=[0,0]
P2issent=[0,0]
house_num=[0,0]
#初始1先发送
whosend=[1,1]
house_is=[0,0]
def process(request, client_address):
    #这五个变量是联系两个客户端的
    global i,Player1,Player2,P1issent,P2issent,whosend,house_num,house_is
    
    print(request,client_address)

    conn = request
    #获得客户端选择的房间
    data = conn.recv(1024).decode()
    house = int(data)
    house_num[house-1] += 1
    #获得是这个房间的第几个人
    if house_num[house-1] == 3:
        #不能超过三个人
        data = 'fulled'
        conn.sendall(bytes(data,encoding='utf-8'))
        return 0
    else:
        i = house_num[house-1]
    #i用来告诉服务端我是谁，this是函数内变量
    this=i
    
    #第一次来的是1号，第二次是2号
    conn.sendall(bytes('欢迎|%d号玩家来到%d号房间.'%(i,house),encoding='utf-8'))
    flag = True
    #开始等待客户端发消息
    while flag:
        #接受消息:
        #轮流发送消息
        print('this:',this,'whosend:',whosend[house-1],'P1issent:',P1issent[house-1]\
              ,'P2issent:',P2issent[house-1])
        if whosend[house-1] == this:
            data = conn.recv(1024).decode()
            #who是哪个客户，data是发送过来的消息
            whichHouse = int(data.split(':')[0])
            who = int(data.split(':')[1])
            data = data.split(':')[2]
            print(whichHouse,who,data)
            #按理来说，1号客户先发送消息，此时2号在等待，1号发送之后2号接受
            #2号变为发送状态，1号变为接受状态
            if data == 'end':
                house_num[house-1] = 0
                Player1[house-1]='0'
                Player2[house-1]='0'
                P1issent[house-1]=0
                house_num[house-1]=0
                P2issent[house-1]=0
                whosend[house-1]=1
                house_is[house-1]=0
                break
            if who==1:
                Player1[house-1]=data
                P1issent[house-1]=1
                whosend[house-1]=2
            else:
                Player2[house-1]=data
                P2issent[house-1]=1
                whosend[house-1]=1
        else:
            whowait = (whosend[house-1])%2+1
            if whowait == 1:
                while not P2issent[house-1]:
                    pass
                print(Player2[house-1])
                conn.sendall(bytes(Player2[house-1],encoding='utf-8'))
                
                P2issent[house-1]=0
            else:
                while not P1issent[house-1]:
                    pass
                print(Player1[house-1])
                conn.sendall(bytes(Player1[house-1],encoding='utf-8'))
                
                P1issent[house-1]=0
 
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(('10.5.247.175',8002))
sk.listen(10)
 
while True:
    r, w, e = select.select([sk,],[],[],1)
    #创建多线程
    if sk in r:
        request, client_address = sk.accept()
        t = threading.Thread(target=process, args=(request, client_address))
        t.daemon = False
        t.start()
 
sk.close()
