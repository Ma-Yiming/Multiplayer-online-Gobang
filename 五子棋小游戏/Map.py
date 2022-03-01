import pygame
from pygame.locals import *

#棋盘相关
class Map():
    def __init__(self,length):
        self.length=length*(Line_num+1) #总体长度为length*16，与画布长度平齐
        self.Rec_size=length #空格间距为length
        self.map=[[0 for x in range(Line_num)] for y in range(Line_num)]#创建一个棋盘地图，用于记录之后下过的位置
        self.steps=[]#记录每次下的棋，与self.map配合使用就能知道棋局情况
        self.turn=1
        player_one=(0,0,0)
        player_two=(255,255,255)
        self.player_color=[player_one,player_two]
    #重置棋盘
    def reset(self):
        #地图无棋子处理
        for i in range(Line_num):
            for j in range(Line_num):
                self.map[i][j]=0
        self.steps=[]
        self.turn=1

    #轮流设置
    def nextwho(self,turn):
        if turn == 1:
            return 2
        else:
            return 1

    def Isempty(self,x,y):
        if self.map[y-1][x-1]==0:
            return 1
        else:
            return 0
    def IsinMap(self,x,y):
        if x<1 or x>15 or y<1 or y>15:
            return 0
        else:
            return 1
        
    def Mapwhere(self,x,y):
        #根据x,y返回当前点对应的实际位置
        map_x=x*Map_size
        map_y=y*Map_size
        return (map_x,map_y,Map_size,Map_size)
    
    def MapPos(self,map_x,map_y):
        #根据实际位置返回坐标
        x=round(map_x / Map_size)
        y=round(map_y / Map_size)
        return (x,y)
    
    def click(self,x,y):
        #通过点击获得对应的x,y
        #注意的是，这里x,y应以(1,1)为原点
        #self.map[y][x]=type.value
        self.steps.append((x,y))
        self.map[y-1][x-1]=self.turn
        self.turn=self.nextwho(self.turn)
        
    def drawbackground(self,screen):
        color=(0,0,0) #设置线为黑色
        #绘制水平的线
        for i in range(Line_num):#15条线，所以15次
            start_pos=(self.Rec_size,self.Rec_size+self.Rec_size*i)
            end_pos=(self.length-self.Rec_size,self.Rec_size+self.Rec_size*i)
            if i == Line_num//2:#中间那条线增粗
                width=3
            else:
                width=2
            pygame.draw.line(screen,color,start_pos,end_pos,width)#绘制线
        #绘制垂直的
        for i in range(Line_num):
            start_pos=(self.Rec_size+self.Rec_size*i,self.Rec_size)
            end_pos=(self.Rec_size+self.Rec_size*i,self.length-self.Rec_size)
            if i == Line_num//2:
                width=3
            else:
                width=2
            pygame.draw.line(screen,color,start_pos,end_pos,width)
        #绘制完之后，棋盘相当于从(1,1)开始，(0,0)作为了画布起点
        #绘制棋盘上的点
        pos = [(4,4),(12,4),(4,12),(12,12),(8,8)]
        for (x,y) in pos:
            pygame.draw.circle(screen,color,[x*self.Rec_size,y*self.Rec_size],10,0)
        #更新到窗口上
        pygame.display.flip()
    def drawChess(self,screen):
        #for i in range(len(self.steps)):
        x,y=self.steps[-1]
        map_x,map_y,width,height=self.Mapwhere(x,y)
        pos,radius = (map_x,map_y),Chess_R
        flag=self.map[y-1][x-1]
        pygame.draw.circle(screen,self.player_color[flag-1],pos,radius)
        #print("radius yes")
        pygame.display.flip()
    def Drawall(self,screen):
        screen.fill((213,176,146))
        self.drawbackground(screen)
        for chess in self.steps:
            x,y = chess
            map_x,map_y,width,height=self.Mapwhere(x,y)
            pos,radius = (map_x,map_y),Chess_R
            flag=self.map[y-1][x-1]
            pygame.draw.circle(screen,self.player_color[flag-1],pos,radius)
    def Draw_turns(self,screen,map_now,steps_now):
        font = pygame.font.SysFont(None, Map_size*2//3)
        self.map = map_now
        self.steps = steps_now
        screen.fill((213,176,146))
        self.drawbackground(screen)
        for i,chess in enumerate(self.steps):
            x,y = chess
            map_x,map_y,width,height=self.Mapwhere(x,y)
            pos,radius = (map_x,map_y),Chess_R
            flag=self.map[y-1][x-1]
            if flag == 1:
                op_turn = 2
            else:
                op_turn = 1
            pygame.draw.circle(screen,self.player_color[flag-1],pos,radius)
            #字体颜色与背景相反，背景与背景相同（是一个矩形）
            msg_image = font.render(str(i+1),True,self.player_color[op_turn-1],\
                                    self.player_color[flag-1])
            #获得字的句柄，设置中心位置
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.center = pos
            #写字
            screen.blit(msg_image, msg_image_rect)
            pygame.display.flip()
    def init_screen(self,screen):
        screen.fill((213,176,146))
        self.drawbackground(screen)
        pygame.display.flip()
            
Map_size = 50  #表示棋盘每一格的宽度
Line_num = 15 #棋盘的大小（线的多少）
Screen_size = Map_size*(Line_num+1) #表示画布的大小，因为棋盘是14*14格，15*15线，两边都空一格，所以乘以16
Chess_R = Map_size//2-5 #每一个棋子的半径
