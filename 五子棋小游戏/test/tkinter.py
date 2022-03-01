import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pandas as pd


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.frame_top = tk.Frame(width=600, height=90)
        self.frame_center = tk.Frame(width=600, height=180)
        self.frame_bottom = tk.Frame(width=600, height=90)
        
        self.lb_tip = tk.Label(self.frame_top,text="查询棋局")
        self.string = tk.StringVar()
        self.string.set('')
        self.ent_find_name = tk.Entry(self.frame_top, textvariable=self.string)
        self.btn_query = tk.Button(self.frame_top,text="查询",command=self.query)

        self.lb_tip.grid(row=0,column=0,padx=15,pady=30)
        self.ent_find_name.grid(row=0,column=1,padx=15,pady=30)
        self.btn_query.grid(row=0,column=2,padx=15,pady=30)

        self.btn_add = tk.Button(self.frame_bottom,text="查看本次棋局")
        self.btn_add.bind('<Button-1>',self.add_event)
        self.btn_add.grid(row=0,column=0,padx=15,pady=30)


        self.tree = ttk.Treeview(self.frame_center,show="headings",height=8,\
                                 columns=('a','b','c','d'))
        self.vbar = ttk.Scrollbar(self.frame_center,orient=tk.VERTICAL,\
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vbar.set)
        self.tree.column("a", width=80, anchor="center")
        self.tree.column("b", width=120, anchor="center")
        self.tree.column("c", width=120, anchor="center")
        self.tree.column("d", width=120, anchor="center")
        self.tree.heading("a", text="时间")
        self.tree.heading("b", text="玩家一")
        self.tree.heading("c", text="玩家二")
        self.tree.heading("d", text="获胜者")
        self.tree["selectmode"] = "browse"
        self.tree.bind("<ButtonRelease-1>", self.item_click)
        self.tree.grid(row=0, column=0, sticky=tk.NSEW, ipadx=10)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.frame_top.grid(row=0,column=0,padx=60)
        self.frame_center.grid(row=1,column=0,padx=60,ipadx=1)
        self.frame_bottom.grid(row=2,column=0,padx=60)
        self.frame_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.data_frame = None
        self.item_selection = ""
        self.query()
        self.mainloop()
        
    def item_click(self, event):
        try:
            selection = self.tree.selection()[0]
            data = self.tree.item(selection, "values")
            self.item_selection = data[0]
        except IndexError:
            tkinter.messagebox.showinfo("警告", "范围异常，请重新选择！")
    def query(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        query_info = self.ent_find_name.get()
        self.string.set('')
        df = self.data_frame = pd.read_excel("data/users_data.xlsx")
        if query_info is None or query_info == "":
            pass
        else:
            df = self.data_frame.loc[df["课程名称"].str.contains(query_info)]
        for index, row in df.iterrows():
            data = [row["课程编号"], row["课程名称"], row["上课地点"], row["上课时间"]]
            self.tree.insert("", "end", values=data)
    def add(self):
        pass
    def add_event(self,event):
        print(event.x,event.y)
        self.add()
asdf=MainWindow() 
