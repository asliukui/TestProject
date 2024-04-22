import os
import re
import pandas as pd
import sys

if len(sys.argv) > 1:
    param = sys.argv[1]
    print("传递的参数:", param)
else:
    print("没有传递参数")
# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 指定要删除的文件名
file_to_delete = "date_bk.xlsx"
# 组合成完整的文件路径
FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
FILE_URL_IN= same_level_directory+"/"+"bbb.xlsx"
# 设置显示完整的列
pd.set_option('display.max_columns', None)
# 设置显示完整的行
pd.set_option('display.max_rows', None)

flagArr = ["主键", "sum", "YES", "NO", "是", "否", "主键不空", "主键唯一", "码值"]
tableName = ["", ""]
PRIMARY_KEY = "主键"

# STRING_URL = r'C:\Users\asliu\Desktop\aaa.xlsx'
# outputpath = r"C:\Users\asliu\Desktop\a_bk.xlsx"


class DfExcle:
    old_cols_arr = ["字段名称", "中文名称", "字段类型", "可空", "", "备注", "返回目录"]
    new_cols_arr = ["new_tab", "old_tab", "old_field", "where", "intent1", "sql1"
        , "intent2", "sql2", "intent3", "sql3"]

    def __init__(self, str_url):
        self.df = pd.read_excel(str_url)
        self.old_cols_arr[4] = self.df.columns[4]
        self.col_num_field_en = self.df.columns.get_loc(self.old_cols_arr[0])
        self.col_num_field_cn = self.df.columns.get_loc(self.old_cols_arr[1])
        self.col_num_field_type = self.df.columns.get_loc(self.old_cols_arr[2])
        self.col_num_field_isnull = self.df.columns.get_loc(self.old_cols_arr[3])
        self.col_num_field_mid_tab = self.df.columns.get_loc(self.old_cols_arr[4])
        self.col_num_field_remark = self.df.columns.get_loc(self.old_cols_arr[5])
        self.col_num_field_bk = self.df.columns.get_loc(self.old_cols_arr[6])

        self.col_num_new_tab = self.df.columns.get_loc(self.new_cols_arr[0])
        self.col_num_old_tab = self.df.columns.get_loc(self.new_cols_arr[1])
        self.col_num_old_field = self.df.columns.get_loc(self.new_cols_arr[2])
        self.col_num_where = self.df.columns.get_loc(self.new_cols_arr[3])
        self.col_num_intent1 = self.df.columns.get_loc(self.new_cols_arr[4])
        self.col_num_sql1 = self.df.columns.get_loc(self.new_cols_arr[5])
        self.col_num_intent2 = self.df.columns.get_loc(self.new_cols_arr[6])
        self.col_num_sql2 = self.df.columns.get_loc(self.new_cols_arr[7])
        self.col_num_intent3 = self.df.columns.get_loc(self.new_cols_arr[8])
        self.col_num_sql3 = self.df.columns.get_loc(self.new_cols_arr[9])

    # 计划写2个内部类，1个封装所有df，另一个封装df对应的属性 class FieldBean，方便调用时直接传值。
    # def init_df(self,file_path:str):
    #     # 读取 Excel 文件，获取所有sheets
    #     self.data = pd.read_excel(file_path, sheet_name=None)
    #
    #     # 存储每个 sheet 的 DataFrame ,容器
    #     self.sheets_data = {}
    #
    #     # 遍历每个 sheet
    #     for sheet_name in self.data.keys():
    #         self.sheets_data[sheet_name] = self.data[sheet_name]

def del_file(outputpath: str):
    if os.path.exists(outputpath):
        # 如果文件存在，则删除它
        os.remove(outputpath)
        print(f"文件 {outputpath} 已删除。")
    else:
        print(f"文件 {outputpath} 不存在。")


# 空串校验
def isNotNUll(str):
    if str is None:
        return False
    elif str == "nan":
        return False
    elif len(str.strip()) == 0:
        return False
    else:
        return True


# 测试意图,字段英文名，中文名，标示
def test_intent(field_en: str, field_cn: str, flag=''):
    if len(field_cn)>8:
        index = re.search(r'[a-zA-Z]', field_cn).start()
        if index >1:
            field_cn = field_cn[:index]
        else:
            field_cn = field_cn[:8]
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


# print(test_intent("是否恢复停息期间利息标识","re_interest_flag"))

# 判定值不为空
def str_is_null(tabName: str, felid: str, rowBean,field_not_null=True):
    if isNotNUll(rowBean.loc[ex.new_cols_arr[3]]) == False:  # 无where条件
        strSql = f"select count(1) as tcount from {tabName} where nvl({felid},'') !=''"
    elif isNotNUll(rowBean.loc[ex.new_cols_arr[3]]) and isNotNUll(
            rowBean.loc[ex.new_cols_arr[2]]) == False:  # where列非空，old_field 空
        if field_not_null:
            strSql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[ex.new_cols_arr[1]]} t2 where {rowBean.loc[ex.new_cols_arr[3]]} and nvl({felid},'') !='' "
        else:
            strSql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[ex.new_cols_arr[1]]} t2 where {rowBean.loc[ex.new_cols_arr[3]]}"
    elif isNotNUll(rowBean.loc[ex.new_cols_arr[3]]) and isNotNUll(
            rowBean.loc[ex.new_cols_arr[2]]) == True:  # where列非空，old_field 非空
        if field_not_null:
            strSql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[ex.new_cols_arr[1]]} t2 where {rowBean.loc[ex.new_cols_arr[3]]} and nvl({felid},'') =nvl({rowBean.loc[ex.new_cols_arr[2]]},'')"
        else:
            strSql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[ex.new_cols_arr[1]]} t2 where {rowBean.loc[ex.new_cols_arr[3]]} and t1.{felid} =t2.{rowBean.loc[ex.new_cols_arr[2]]}"
    else:
        strSql = f"select count(1) as tcount from {tabName}"
    return strSql


# 判定主键准确性
def primary_key_is_right():
    strSql = ""
    return strSql


# 判定主键唯一
def primary_key_only():
    strSql = ""
    return strSql


# 总条数,tab_index: {0:new_tab , 1-old_tab , 2-select 0 , 3-select ''}
def tabCounts(row, tab_index=2):
    if tab_index in [0,1]:
        return f"select count(1) as tcount from {row[ex.new_cols_arr[tab_index]]}"
    elif tab_index == 2:
        return f"select 0 as tcount"
    else:
        return f"select '' as tcount"


# 初始化行列值，用于遍历
rowIndex = 0
colIndex = 0
# 加载excle文件，生成DateFrame对象
ex = DfExcle(FILE_URL_IN)
df = ex.df
pd.options.mode.copy_on_write = True
# 总行数和总列数
df_rows = df.shape[0]
df_cols = df.shape[1]
# print("字段数：",df_rows-1)
# df.loc["关联关系"] = df["关联关系"].astype(str).str.replace("nan","")
# df.iloc[:, 20] = df.iloc[:, 20].str.replace("nan",'')
# df.loc[:["A","B"]] = df.loc[:["A","B"]].astype(str).str.replace("nan","")

# 选择 0 到 最大 列,替换nan none 为"",并转换成字符串格式
df = df.iloc[:, 0:df_cols].fillna("").astype(str)
columnNameArr = ["字段名称", "中文名称", "字段类型", "可空", "", "备注"
    , "返回目录", "目标表名(t1)", "源表名(t2)", "原表字段", "关联关系"
    , "测试意图", "sql1", "sql2", "sql3"]
for index, row in df.iterrows():
    if row[ex.old_cols_arr[5]] == PRIMARY_KEY:  # 1.主键不为空;2.执行语句
        # print(df.columns.get_loc(columnNameArr[5]))  ##根据列名获取当前列数
        df.loc[index, df.columns[ex.col_num_intent1]] = test_intent("", "", flagArr[6])  #
        df.loc[index, df.columns[ex.col_num_sql1]] = str_is_null(row.iloc[7], row.iloc[0],
                                                                 row)  # 测试意图,主键
        df.loc[index, df.columns[ex.col_num_sql2]] = tabCounts(row, 0)
    elif row[columnNameArr[3]] == flagArr[3] or row[columnNameArr[3]] == flagArr[5]:  # 1.测试意图,判断非主键，不可为空 2.执行sql语句
        df.loc[index, df.columns[ex.col_num_intent1]] = test_intent(row.iloc[0], row.iloc[1],
                                                                    flagArr[3])
        df.loc[index, df.columns[ex.col_num_sql1]] = str_is_null(row.iloc[7], row.iloc[0],
                                                                 row)  # sql判定值不为空
        df.loc[index, df.columns[ex.col_num_sql2]] = tabCounts(row, 0)
    elif row[columnNameArr[3]] == flagArr[2] or row[columnNameArr[3]] == flagArr[4]:  # 1.测试意图,判断非主键，可空 2.执行sql语句
        df.loc[index, df.columns[ex.col_num_intent1]] = test_intent(row.iloc[0], row.iloc[1],
                                                                    flagArr[2])
        df.loc[index, df.columns[ex.col_num_sql1]] = str_is_null(row.iloc[7], row.iloc[0],
                                                                 row,False)  # sql判定值不为空
        df.loc[index, df.columns[ex.col_num_sql2]] = tabCounts(row, 0)
    elif index == df_rows - 1:  # 1.测试意图,统计table数据总量 2.执行sql语句
        df.loc[index, df.columns[ex.col_num_intent1]] = test_intent("", "",
                                                                    flagArr[1])
        df.loc[index, df.columns[ex.col_num_sql1]] = tabCounts(row, 0)
        df.loc[index, df.columns[ex.col_num_sql2]] = tabCounts(row, 1)

# 删除之前是生成的文件，并重新生成文件
del_file(FILE_URL_OUT)
df.to_excel(FILE_URL_OUT, index=False)
