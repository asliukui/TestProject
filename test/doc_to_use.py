import pandas as pd
df = pd.read_excel("STRING_URL")
df.head()#查看前几行数据
#替换nan
df.loc[:["A","B"]] = df.loc[:["A","B"]].astype(str).str.replace("nan","")
###1查询
##1.1使用单值查询。
df.loc["rowindex1":"columnindex1"]
df.loc["rowindex1":["columnindex1","columnindex2"]]

##1.2.使用值列表批量查询
df.loc[["rowindex1","rowValue2"]:["columnindex1","columnindex2"]]

##1.3.使用区间进行范围查询
#按照index行区间进行查询
df.loc["rowindex1":"rowindex2","columnindex1"]
#按照index列区间进行查询
df.loc["rowindex1","columnindex1":"columnindex2"]

##1.4.使用条件查询，重要
df.loc[df["money"]>500:]    #查询列名为money，值大于500的所有行（限定行条件，列取全部）
#多条件查询
df.loc[(df["money"]<500) & (df["money"])>300&(df["name"] == "穷")]

##1.5.调用函数查询
df.loc[lambda df :(df["money"]<500) & (df["money"]>300),:]
def query(df):
    return df.index.str.startswith("1") & df["备注"].notnull()
#传递函数做为参数，不需要传参数，获得满足条件的行 和 所有列
df.loc[query,:]



###查询2
#查询一列
df["列名"]
#查询多列
df[["列名1","列名2"]]
#查询一行 [行号index]
df.loc[1]
#查询多行,1-3行
df.loc[1:3]

##根据列名获取当前列的index
print(df.columns.get_loc("new_tab"))

#添加列
# 第一种方法：创建一个示例 DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)


# 第二种方法：定义要添加的空列名列表
new_columns = ['C', 'D', 'E']

# 使用 assign 方法批量添加空列
df = df.assign(**{column: None for column in new_columns})