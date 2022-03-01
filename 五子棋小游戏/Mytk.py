import tkinter as tk
from tkinter import ttk
import numpy as np
import tkinter.messagebox
import pandas as pd
import pygame
from pygame.locals import *

class Mytk(tk.Tk):
    def __init__(self,map1,screen,map_list,steps_list):
        super().__init__()
        self.lis=[[]]
        self.select=0
        self.map1=map1
        self.screen=screen
        self.map_list=map_list
        self.steps_list=steps_list
        frame_top = tk.Frame(width=600, height=90)
        frame_center = tk.Frame(width=600, height=180)
        frame_bottom = tk.Frame(width=600, height=90)

        lb_tip = tk.Label(frame_top, text="选择棋盘")
        self.string = tk.StringVar()
        self.string.set('')
        self.end_find_name = tk.Entry(frame_top, textvariable=self.string)
        btn_query = tk.Button(frame_top, text="查询", command=self.query)
        lb_tip.grid(row=0,column=0,padx=15,pady=30)
        self.end_find_name.grid(row=0,column=1,padx=15,pady=30)
        btn_query.grid(row=0,column=2,padx=15,pady=30)

        frame_top.grid()
        frame_center.grid()
        frame_bottom.grid()

        self.tree = ttk.Treeview(frame_center,columns=['时间','玩家一','玩家二','获胜者'],show="headings")
        self.tree.column('0',width=200,anchor='center')
        self.tree.column('1',width=100,anchor='center')
        self.tree.column('2',width=100,anchor='center')
        self.tree.column('3',width=100,anchor='center')
        self.tree.heading('0',text='时间')
        self.tree.heading('1',text='玩家一')
        self.tree.heading('2',text='玩家二')
        self.tree.heading('3',text='获胜者')

        self.lis = self.exceltolis()
        self.txtname=[]
        for each in self.lis:
            self.txtname.append(each[0])
        #print(self.txtname)
        for each in self.lis:
            self.tree.insert('','end',values=each)
        self.tree.bind('<ButtonRelease-1>',self.treeviewClick)
        self.tree.grid()
        self.mainloop()
    def exceltolis(self):
        lis=[[]]
        df = pd.read_excel("data/users_data.xlsx")
        for row in df.index.values:
            lis.append([])
            for i in range(4):
                lis[row].append(df.iloc[row,i])
        lis.pop()
        return lis
    def treeviewClick(self,event):
        try:
            for item in self.tree.selection():
                item_text = self.tree.item(item,'values')
                
                #获得文件对应下标
                self.select=self.txtname.index(item_text[0])
                self.map1.Draw_turns(self.screen,\
                                     self.map_list[self.select],\
                                     self.steps_list[self.select])
        except:
            pass
    def delButton(self,tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)
    def query(self):
        #清空
        self.delButton(self.tree)
        query_info = self.end_find_name.get()
        #print(query_info,self.lis)
        self.string.set('')
        #支持模糊查找，空则重置，不空则进行模糊查找
        if query_info is None or query_info == "":
            for each in self.lis:
                self.tree.insert('','end',values=each)
        else:
            #循环每一个元素，判断是否是其子字符串
            for each in self.lis:
                for each_item in each:
                    if query_info in each_item:
                        self.tree.insert('','end',values=each)
                        break
            
        

