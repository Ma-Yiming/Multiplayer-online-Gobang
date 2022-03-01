import pygame
import time
import pandas as pd
import sys

class Text:
    def __init__(self):
        self.width=300
        self.height=70
        self.x1pos=250+90
        self.y1pos=420+21
        self.txt1=""
        self.x2pos=250+90
        self.y2pos=490+25
        self.txt2=""
        self.font=pygame.font.Font(None,40)
        self.block=1
        self.running =True
        self.endwinner=0
        
    def draw(self,screen):
        screen.blit(img_name,(Textpos_L,Textpos_U))
        #print(222)
        #surface=pygame.Surface((self.width,self.height))
        
        textfont1 = self.font.render(self.txt1,True,(0,0,0))
        
        textfont2 = self.font.render(self.txt2,True,(0,0,0))
        
        screen.blit(textfont1,\
                    (self.x1pos,self.y1pos+10))
        screen.blit(textfont2,\
                    (self.x2pos,self.y2pos+10))
        
    def keydown(self,event):
        unicode = event.unicode
        key = event.key
        #print(self.block)
        if key == 8:
            if self.block == 1:
                self.txt1=self.txt1[:-1]
                return
            if self.block == 2:
                self.txt2=self.txt2[:-1]
                return
        if key == 301:
            return
        if key == 13:
            if self.block == 1:
                self.block=2
            else:
                self.running = False
            return
        if self.block==1:
            if key==1073741903 or key==1073741903 or key==1073741903\
            or key==1073741903 :
                pass
            elif unicode !="" and len(self.txt1)<12:
                character = unicode
                self.txt1+=character
            else:
                pass
        else:
            if key==1073741903 or key==1073741903 or key==1073741903\
            or key==1073741903 :
                pass
            elif unicode !="" and len(self.txt2)<12:
                character = unicode
                self.txt2+=character
            else:
                pass
    def txt_to_excel(self):
        data = pd.read_csv(r'data\users.txt',encoding='gbk')
        data_col=['时间','玩家一','玩家二','胜利者']
        data_lis=[]
        data_doc={'时间':[],'玩家一':[],'玩家二':[],'胜利者':[]}
        for index in data.index:
            data_lis.append(((list(data.loc[index]))[0].split("："))[1].strip(' '))
        for key,item in enumerate(data_lis):
            data_doc[data_col[key%4]].append(item)
        df = pd.DataFrame(data_doc)
        df_new=df.set_index('时间')
        df_new.to_excel(r'data\users_data.xlsx')
    def resave(self,Map,steps):
        self.winner=[self.txt1,self.txt2]
        #构造一个特定对应的文件名称来记录棋局情况
        time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        filename="data\\chess_history\\"+time_now+".txt"
        tem=''
        each=filename.split(':')
        for i in each:
            tem+=i
        filename=tem
        #编码问题
        with open("data/users.txt","a") as fp:
            fp.write("时间： "+time_now+\
                     "\n"+"玩家一： "+self.txt1+"\n"+\
                     "玩家二： "+self.txt2+"\n"+"胜利者："\
                     +self.winner[self.endwinner]+"\n")
        Map_tem=[]
        for i in Map:
            Map_line="".join(str(each) for each in i)
            Map_tem.append(Map_line)
        Map=''.join(str(each) for each in Map_tem)
        steps=''.join(str(each) for each in steps)
        #print(Map,steps)
        with open(filename,'w') as fp2:
            fp2.write(Map)
            fp2.write('\n')
            fp2.write(steps)
        self.txt_to_excel()
    def mousedown(self,screen):
        self.draw(screen)
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                mouse_x,mouse_y = pygame.mouse.get_pos()
                if Textone_L < mouse_x and mouse_x < Textone_R \
                   and Textone_U < mouse_y and mouse_y < Textone_D\
                   and event.type == pygame.MOUSEBUTTONDOWN:
                    self.block=1
                elif Texttwo_L < mouse_x and mouse_x < Texttwo_R \
                   and Texttwo_U < mouse_y and mouse_y < Texttwo_D\
                   and event.type == pygame.MOUSEBUTTONDOWN:
                    self.block=2
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.keydown(event)
                    self.draw(screen)
                    pygame.display.flip()

img_name = pygame.image.load("img/name.png")
#文本框位置
Textpos_L = 50
Textpos_U = 300
#文本框中两个输入框对应的位置
Textone_L = 240
Textone_R = 530
Textone_U = 435
Textone_D = 470
Texttwo_L = 240
Texttwo_R = 530
Texttwo_U = 520
Texttwo_D = 540
