import pandas as pd

data = pd.read_csv(r'data\users.txt',encoding="gbk")
data_col=['时间','玩家一','玩家二','胜利者']
data_lis=[]
data_doc={'时间':[],'玩家一':[],'玩家二':[],'胜利者':[]}
for index in data.index:
    data_lis.append(((list(data.loc[index]))[0].split("："))[1].strip(' '))
for key,item in enumerate(data_lis):
    data_doc[data_col[key%4]].append(item)
df = pd.DataFrame(data_doc)
df_new=df.set_index('时间')
df_new.to_excel(r'data\uses_data.xlsx')

    
