import os

import pandas as pd

columnNameArr = ["字段名称", "中文名称", "字段类型", "可空", "", "备注"
    , "返回目录", "目标表名(t1)", "源表名(t2)","原表字段", "关联关系"
    , "测试意图", "sql1", "sql2", "sql3"]
old_cols_arr = ["字段名称", "中文名称", "字段类型", "可空", "", "备注","返回目录"]
new_cols_arr = ["new_tab", "old_tab","old_field", "where", "intent1", "sql1", "intent2","sql2", "intent3", "sql3"]
flagArr = ["主键", "sum", "YES", "NO", "是", "否", "主键不空", "主键唯一", "码值"]
tableName = ["", ""]
PRIMARY_KEY = "主键"
# 文件地址
STRING_URL = r'C:\Users\asliu\Desktop\aaa.xlsx'
outputpath = r"C:\Users\asliu\Desktop\a_bk.xlsx"

def test_intent(field_en: str, field_cn: str, flag=''):
    if flag == flagArr[0]:  # 主键
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[1]:  # sum
        strlog = f"验证：目标表与源表迁移数据总数的一致性"
    elif flag == flagArr[2] or flag == flagArr[4]:  # YES 是
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[3] or flag == flagArr[5]:  # NO 否
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[6]:  # 主键不空
        strlog = f"验证：主键不为空"
    elif flag == flagArr[7]:  # 主键唯一
        strlog = f"验证：目标表数据的唯一性"
    elif flag == flagArr[8]:  # 码值
        strlog = f"验证：{field_en}({field_cn})码值在落标码值范围内"
    else:
        strlog = ""
    return strlog

def test_intent1(df,index, flag=''):
    field_en=df[old_cols_arr[0]]
    field_cn=df[old_cols_arr[1]]
    intentStr= "intent"+str(index)
    strlog=""
    if flag == flagArr[0]:  # 主键
        # strlog = f"验证：{field_en}({field_cn})取值的正确性"
        # df.loc[:intentStr] = f"验证：{df[old_cols_arr[0]]}({df[old_cols_arr[1]]})取值的正确性"
        print(f"验证：{df[old_cols_arr[0]]}({df[old_cols_arr[1]]})取值的正确性")
    elif flag == flagArr[1]:  # sum
        strlog = f"验证：目标表与源表迁移数据总数的一致性"
    elif flag == flagArr[2] or flag == flagArr[4]:  # YES 是
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[3] or flag == flagArr[5]:  # NO 否
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[6]:  # 主键不空
        strlog = f"验证：主键不为空"
    elif flag == flagArr[7]:  # 主键唯一
        strlog = f"验证：目标表数据的唯一性"
    elif flag == flagArr[8]:  # 码值
        strlog = f"验证：{field_en}({field_cn})码值在落标码值范围内"
    else:
        strlog = ""
    # print(df)
    return df



df = pd.read_excel(STRING_URL)
#主键操作

df.loc[new_cols_arr[4]]=test_intent1(df.loc[df[columnNameArr[5]] == flagArr[0]],1,flagArr[0])
df.head()
# print(df_key)