import socket
import pygame
import threading
from pygame.locals import *
from Game import *
import time
import sys

class Client():
    def __init__(self,ip_port,mapclass,screen,house):
        #第几个房间的第几号
        self.num = ''
        self.house = house
        self.img=[img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12]
        self.iswaiting = 0
        self.screen=screen
        self.map1=mapclass
        #连接
        self.sk = socket.socket()
        self.sk.connect(ip_port)
        self.sk.settimeout(5)
        self.SendMyHouse()
        #设置下棋需要变量
        self.White_win=0
        self.Black_win=0
        self.winner=0
        self.end = 0
        self.turn = 1
        #返回上一级使用
        self.isplay = 1
        #开始发消息
        self.round()
    def wait(self):
        while self.isplay:
            try:
                #一直得带接受信息
                data = self.sk.recv(1024).decode()
                #print(data)
                #房间满了就退出
                if data == 'fulled':
                    self.isplay = 0
                    break
                #第一次接收时获得标号
                if self.num == '':
                    self.num=((data.split('|')[1])[0])
                    break
                #处理数据
                x=int(data.split(',')[0])
                y=int(data.split(',')[1])
                if self.isplay:
                    self.map1.click(x,y)
                    #print(self.map1.steps)
                    self.map1.drawChess(self.screen)
                if self.IsEnd(x,y):
                    #这里其实已经变成1了，这样写为了逻辑上清楚点
                    self.end = 1 
                if self.turn == 1:
                    self.turn = 2
                else:
                    self.turn = 1
            except:
                #不会进来
                pygame.display.flip()
                continue
    def thread(self):
        t = threading.Thread(target=self.wait)
        t.start()
    def round(self):
        self.wait()
        #让发送和接受是两个线程
        self.thread()
        #一号玩家
        if self.num == '1':
            while self.isplay:
                running = True
                while running:
                    if self.isplay == 0:
                        break
                    if self.end == 1:
                        self.End()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN and \
                           self.turn == 1:
                            x,y=self.clickwhere()
                            running = False
                #发送信息
                if (x is not -1) and (y is not -1):
                    send_data = str(x)+','+str(y)
                    self.sk.sendall(bytes(str(self.house)+':'+self.num+':'+send_data,encoding='utf-8'))
                    self.turn = 2
                if self.isplay == 0:
                        break
                if self.end == 1:
                    self.End()
        #二号玩家
        elif self.num == '2':
            while self.isplay:
                running = True
                while running:
                    if self.isplay == 0:
                        break
                    if self.end == 1:
                        self.End()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN and\
                           self.turn == 2:
                            x,y=self.clickwhere()
                            running = False
                if (x is not -1) and (y is not -1):
                    send_data = str(x)+','+str(y)
                    self.sk.sendall(bytes(str(self.house)+':'+self.num+':'+send_data,encoding='utf-8'))
                    self.turn = 1
                if self.isplay == 0:
                    break
                if self.end == 1:
                    self.End()
        elif self.num == '':
            self.End()
    #获取点击位置并绘图判断是否结束
    def clickwhere(self):
        map_x,map_y=pygame.mouse.get_pos()
        x,y=self.map1.MapPos(map_x,map_y)
        #print(map_x,"-----",map_y,"-----",x,"-----",y)
        #下边的先后顺序不能反，不然会有数组越界报错
        if self.map1.IsinMap(x,y) and self.map1.Isempty(x,y):
            self.map1.click(x,y)
            if not self.IsEnd(x,y):
                print(11111)
                self.map1.drawChess(self.screen)
                return (x,y)
        if self.end:
            if self.White_win == 5:
                self.winner = 0
            else:
                self.winner = 1
            self.White_win=0
            self.Black_win=0
            self.map1.drawChess(self.screen)
            return (x,y)
        #如果不是预期
        return (-1,-1)
                
    #四种方向的结束条件
    def IsEnd(self,x,y):
        for i in range(-4,5):
            if x+i > 0 and x+i < 16:
                #print(x+i,self.map1.map[y-1][x+i-1])
                if self.map1.map[y-1][x+i-1]==1:
                    self.Black_win=0
                    self.White_win+=1
                elif self.map1.map[y-1][x+i-1]==2:
                    self.White_win=0
                    self.Black_win+=1
                else:
                    self.White_win=0
                    self.Black_win=0
            if self.White_win==5:
                self.end = 1
                return 1
            if self.Black_win==5:
                self.end = 1
                return 2
        self.White_win=0
        self.Black_win=0
        for j in range(-4,5):
            if y+j > 0 and y+j < 16:
                if self.map1.map[y+j-1][x-1]==1:
                    self.Black_win=0
                    self.White_win+=1
                elif self.map1.map[y+j-1][x-1]==2:
                    self.White_win=0
                    self.Black_win+=1
                else:
                    self.White_win=0
                    self.Black_win=0
            if self.White_win==5:
                self.end = 1
                return 1
            if self.Black_win==5:
                self.end = 1
                return 2
        #print(self.White_win,self.Black_win)
        self.White_win=0
        self.Black_win=0
        for m in range(-4,5):
            if y+m > 0 and y+m < 16 and x+m > 0 and x+m < 16:
                if self.map1.map[y+m-1][x+m-1]==1:
                    self.Black_win=0
                    self.White_win+=1
                elif self.map1.map[y+m-1][x+m-1]==2:
                    self.Black_win+=1
                    self.White_win=0
                else:
                    self.White_win=0
                    self.Black_win=0
            if self.White_win==5:
                self.end = 1
                return 1
            if self.Black_win==5:
                self.end = 1
                return 2
        #print(self.White_win,self.Black_win)
        self.White_win=0
        self.Black_win=0
        for n in range(-4,5):
            if y-n > 0 and y-n < 16 and x+n > 0 and x+n < 16:
                if self.map1.map[y-n-1][x+n-1]==1:
                    self.Black_win=0
                    self.White_win+=1
                elif self.map1.map[y-n-1][x+n-1]==2:
                    self.Black_win+=1
                    self.White_win=0
                else:
                    self.White_win=0
                    self.Black_win=0
           # print(self.White_win,self.Black_win)
            if self.White_win==5:
                self.end = 1
                return 1
            if self.Black_win==5:
                self.end = 1
                return 2
        #print(self.White_win,self.Black_win)
        self.White_win=0
        self.Black_win=0
        self.end = 0
        return 0
    def End(self):
        running = True
        while running:
            for event in pygame.event.get():
                mouse_x,mouse_y = pygame.mouse.get_pos()
                if Former_L < mouse_x and mouse_x < Former_R and \
                   Former_U < mouse_y and mouse_y < Former_D:
                    #达到选中效果
                    self.screen.blit(self.img[9],(Former_L,Former_U))
                    pygame.display.flip()
                    #向服务端返回结束
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        send_data = 'end'
                        self.sk.sendall(bytes(str(self.house)+':'+self.num+':'+send_data,encoding='utf-8'))
                        self.map1.reset()
                        self.map1.init_screen(self.screen)
                        self.isplay = 0
                        running = False
                else:
                    self.screen.blit(self.img[8],(Former_L,Former_U))
                    pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
    #发送房间号
    def SendMyHouse(self):
        data = str(self.house)
        self.sk.sendall(bytes(data,encoding='utf-8'))
#图片导入                    
img1=pygame.image.load("img/upimg.png")
img2=pygame.image.load("img/downimg.png")
img3=pygame.image.load("img/beginup.png")
img4=pygame.image.load("img/begindown.png")
img5=pygame.image.load("img/hisup.png")
img6=pygame.image.load("img/hisdown.png")
img7=pygame.image.load("img/reset.png")
img8=pygame.image.load("img/back.png")
img9=pygame.image.load("img/upformer.png")
img10=pygame.image.load("img/downformer.png")
img11=pygame.image.load("img/uponline.png")
img12=pygame.image.load("img/downonline.png")

#开始游戏图像对应上下左右
Begin_L = 280
Begin_R = 520
Begin_U = 453-100
Begin_D = 547-100
#重新开始图像对应上下左右
Reset_L = 280
Reset_R = 520
Reset_U = 453-100
Reset_D = 547-100
#历史棋局图像对应上下左右
Seehis_L = 280
Seehis_R = 520
Seehis_U = 453+25
Seehis_D = 547+25
#悔棋的上下左右对应范围
Back_L = 790
Back_R = 890
Back_U = 369
Back_D = 431
#返回图像对应上下左右
Former_L = 280
Former_R = 520
Former_U = 453+25
Former_D = 547+25
#联机图像对应上下左右
Online_L = 280
Online_R = 520
Online_U = 453+150
Online_D = 547+150
