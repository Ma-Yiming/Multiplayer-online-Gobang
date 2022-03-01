import pygame
from pygame.locals import *
from Text import *
from Map import *
from Mytk import *
from Client import *
import time
import os
import sys

class Game():
    def __init__(self):
        pygame.init()#pygame初始化
        self.screen=pygame.display.set_mode([Screen_size+100,Screen_size])#设置背景长宽
        self.screen.fill((213,176,146))#设置背景颜色
        pygame.display.set_caption("马艺鸣的五子棋之旅")
        self.img=[img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12\
                  ,img13,img14,img15,img16]
        self.map1=Map(Map_size)#创建一个格子大小为Map_size的map1对象
        self.text=Text()
        self.map1.drawbackground(self.screen)
        self.White_win=0
        self.Black_win=0
        self.winner=0
        self.Play=0#控制是否能下棋
        self.isend = 0
        self.map_list=[]
        self.steps_list=[]
        self.Isbegin()
    #开始选择
    def Isbegin(self):
        running = True
        while running:
            for event in pygame.event.get():
                mouse_x,mouse_y = pygame.mouse.get_pos()
                #print(mouse_x,mouse_y)
                if Begin_L < mouse_x and mouse_x < Begin_R and\
                   Begin_U < mouse_y and mouse_y < Begin_D:
                    self.screen.blit(self.img[3],(Begin_L,Begin_U))
                    pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #输入姓名
                        self.text.mousedown(self.screen)
                        self.Play=1
                        self.screen.fill((213,176,146))
                        self.map1.drawbackground(self.screen)
                        self.screen.blit(self.img[6],(Back_L,Back_U))
                        pygame.display.flip()
                        running = False
                elif Seehis_L < mouse_x and mouse_x < Seehis_R and\
                     Seehis_U < mouse_y and mouse_y < Seehis_D:
                    self.screen.blit(self.img[5],(Seehis_L,Seehis_U))
                    pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #选择历史棋局，返回历史棋局
                        #把棋子的情况导入
                        self.map_list,self.steps_list=self.FiletoList()
                        #初始化界面
                        self.map1.init_screen(self.screen)
                        #tkinter界面
                        mytk=Mytk(self.map1,self.screen,self.map_list,self.steps_list)
                        #当关闭tkinter时初始化界面
                        self.map1.reset()
                        self.map1.init_screen(self.screen)
                elif Online_L < mouse_x and mouse_x < Online_R and\
                     Online_U < mouse_y and mouse_y < Online_D:
                    self.screen.blit(self.img[11],(Online_L,Online_U))
                    pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.map1.init_screen(self.screen)
                        #进入联机
                        self.online()
                else:
                    self.screen.blit(self.img[2],(Begin_L,Begin_U))
                    self.screen.blit(self.img[4],(Seehis_L,Seehis_U))
                    self.screen.blit(self.img[10],(Online_L,Online_U))
                    pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    #获取点击位置并绘图判断是否结束
    def clickwhere(self):
        if self.Play:
            map_x,map_y=pygame.mouse.get_pos()
            x,y=self.map1.MapPos(map_x,map_y)
            #print(map_x,"-----",map_y,"-----",x,"-----",y)
            #下边的先后顺序不能反，不然会有数组越界报错
            if self.map1.IsinMap(x,y) and self.map1.Isempty(x,y):
                self.map1.click(x,y)
                if not self.IsEnd(x,y):
                    self.map1.drawChess(self.screen)
            if self.White_win==5 or self.Black_win==5:
                if self.White_win == 5:
                    self.winner = 0
                else:
                    self.winner = 1
                self.text.endwinner = self.winner
                self.text.resave(self.map1.map,self.map1.steps)
                self.Play=0
                #print("map end")
                self.map1.drawChess(self.screen)
                self.White_win=0
                self.Black_win=0
                self.Isreset()
                
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
                return 1
            if self.Black_win==5:
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
                return 1
            if self.Black_win==5:
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
                return 1
            if self.Black_win==5:
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
                return 1
            if self.Black_win==5:
                return 2
        #print(self.White_win,self.Black_win)
        self.White_win=0
        self.Black_win=0
        return 0
    #重新开始
    def Isreset(self):
        running = True
        while running:
            for event in pygame.event.get():
                #获取当前鼠标位置
                mouse_x,mouse_y = pygame.mouse.get_pos()
                #print(mouse_x,mouse_y)
                if Reset_L < mouse_x and mouse_x < Reset_R and \
                   Reset_U < mouse_y and mouse_y < Reset_D:
                    #达到选中效果
                    self.screen.blit(self.img[1],(Reset_L,Reset_U))
                    pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.map1.reset()
                        #重新绘制
                        self.screen.fill((213,176,146))
                        self.map1.drawbackground(self.screen)
                        self.screen.blit(self.img[6],(Back_L,Back_U))
                        pygame.display.flip()
                        self.Play=1
                        running = False
                elif Former_L < mouse_x and mouse_x < Former_R and \
                   Former_U < mouse_y and mouse_y < Former_D:
                    #达到选中效果
                    self.screen.blit(self.img[9],(Former_L,Former_U))
                    pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.map1.reset()
                        running = False
                        self.map1.init_screen(self.screen)
                        self.Isbegin()
                else:
                    self.screen.blit(self.img[0],(Reset_L,Reset_U))
                    self.screen.blit(self.img[8],(Former_L,Former_U))
                    pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
    def Back(self):
        self.map1.turn=self.map1.nextwho(self.map1.turn)
        history_x,history_y = self.map1.steps[-1]
        self.map1.map[history_y-1][history_x-1] = 0
        self.map1.steps.pop()
        self.map1.Drawall(self.screen)
        self.screen.blit(self.img[6],(Back_L,Back_U))
        pygame.display.flip()
    #把过往的棋盘加到一个列表中去
    def FiletoList(self):
        txtname=[]
        with open("data/users.txt","r") as fp:
            lines = fp.readlines()
        for i in range(1,len(lines),4):
            timelist=(lines[i].split("：")[1]).split(":")
            txtname.append((timelist[0]+timelist[1]+timelist[2])\
                           .strip(" ").strip('\n')+'.txt')
        #print(txtname)
        txt_num=len(txtname)
        #定义存地图和步骤的结构
        map_list=[[[0 for x in range(15)]for y in range(15)]\
                  for z in range(txt_num)]
        steps_list=[[]for x in range(txt_num)]
        #打开文件
        for txt_index,txt in enumerate(txtname):
            with open('data/chess_history/'+txt,"r") as ft:
                lines = ft.readlines()
                for i in range(15):
                    for j in range(15):
                        #lines[0]对应的是存入的map
                        map_list[txt_index][i][j]=int(lines[0][i*15+j])
                #第二行元组字符串转换为元组
                tuple_add=[]
                tuple_x=[]
                tuple_y=[]
                tuple_add=lines[1].split('(')[1:]
                #print(tuple_add)
                for tuple_index in range(len(tuple_add)):
                    if tuple_index == len(tuple_add)-1:
                        tuple_add[tuple_index]=tuple_add[tuple_index].strip('\n')
                    tuple_add[tuple_index]=tuple_add[tuple_index].strip(')')
                #print(tuple_add)
            for i in range(len(tuple_add)):
                #因为右边列表每个只有一个数，所以不用写[0]
                tuple_x,tuple_y=tuple_add[i].split(', ')
                steps_list[txt_index].append((int(tuple_x),int(tuple_y)))
        return map_list,steps_list
    def online(self):
        running = True
        #选择房间
        house = 0
        while running:
            for event in pygame.event.get():
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    if House1_L < mouse_x and mouse_x < House1_R and\
                       House1_U < mouse_y and mouse_y < House1_D:
                        self.screen.blit(self.img[13],(Begin_L,Begin_U))
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.map1.init_screen(self.screen)
                            house = 1
                            player = Client(('10.5.247.175',8002),self.map1,self.screen,house)
                            running = False
                            break
                    elif House2_L < mouse_x and mouse_x < House2_R and\
                         House2_U < mouse_y and mouse_y < House2_D:
                        self.screen.blit(self.img[15],(Seehis_L,Seehis_U))
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.map1.init_screen(self.screen)
                            house = 2
                            player = Client(('10.5.247.175',8002),self.map1,self.screen,house)
                            running = False
                            break
                    else:
                        self.screen.blit(self.img[12],(House1_L,House1_U))
                        self.screen.blit(self.img[14],(House2_L,House2_U))
                        pygame.display.flip()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
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
img13=pygame.image.load("img/uphouse1.png")
img14=pygame.image.load("img/downhouse1.png")
img15=pygame.image.load("img/uphouse2.png")
img16=pygame.image.load("img/downhouse2.png")

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
#房间一图像对应上下左右
House1_L = 280
House1_R = 520
House1_U = 453-100
House1_D = 547-100
#房间二图像对应上下左右
House2_L = 280
House2_R = 520
House2_U = 453+25
House2_D = 547+25
