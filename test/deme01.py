import os
import re
import pandas as pd
import sys

# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 指定要删除的文件名
file_to_delete = "date_bk.xlsx"

# 默认文件路径用于测试代码
FILE_URL_IN = r'C:\Users\asliu\Desktop\中间表-20240422.xlsx'
FILE_URL_OUT = os.path.join(same_level_directory, "a_bk.xlsx")

# 根据传入参数,拼接文件路径
if len(sys.argv) > 1:
    print("传递的参数:", sys.argv)
    param = sys.argv[1]
    FILE_URL_IN = os.path.join(same_level_directory, param)
else:
    print("没有传递参数")

# 设置显示完整的列
pd.set_option('display.max_columns', None)
# 设置显示完整的行
pd.set_option('display.max_rows', None)
pd.options.mode.copy_on_write = True

old_cols_arr = ["字段名称", "中文名称", "字段类型", "可空", "mid_table_name", "备注", "返回目录"]
new_cols_arr = ["new_tab", "old_tab", "old_field", "where", "intent1", "sql1"
    , "intent2", "sql2", "intent3", "sql3"]
flagArr = ["主键", "sum", "YES", "NO", "是", "否", "主键不空", "主键唯一", "码值"]
PRIMARY_KEY = "主键"

def check_array(array1, columns_arr):
    for element in array1:
        if element not in columns_arr:
            return False
    return True

class SheetBean:
    def __init__(self, df):
        self.is_table_sheet=False
        self.columns_arr = list(df.columns)
        if len(df.columns) > 4:
            old_cols_arr[4] = df.columns[4]
        if (check_array(old_cols_arr, self.columns_arr)) and (check_array(new_cols_arr, self.columns_arr)):
            self.is_table_sheet = True
            self.col_num_field_en = df.columns.get_loc(old_cols_arr[0])
            self.col_num_field_cn = df.columns.get_loc(old_cols_arr[1])
            self.col_num_field_type = df.columns.get_loc(old_cols_arr[2])
            self.col_num_field_isnull = df.columns.get_loc(old_cols_arr[3])
            self.col_num_field_mid_tab = df.columns.get_loc(old_cols_arr[4])
            self.col_num_field_remark = df.columns.get_loc(old_cols_arr[5])
            self.col_num_field_bk = df.columns.get_loc(old_cols_arr[6])

            self.col_num_new_tab = df.columns.get_loc(new_cols_arr[0])
            self.col_num_old_tab = df.columns.get_loc(new_cols_arr[1])
            self.col_num_old_field = df.columns.get_loc(new_cols_arr[2])
            self.col_num_where = df.columns.get_loc(new_cols_arr[3])
            self.col_num_intent1 = df.columns.get_loc(new_cols_arr[4])
            self.col_num_sql1 = df.columns.get_loc(new_cols_arr[5])
            self.col_num_intent2 = df.columns.get_loc(new_cols_arr[6])
            self.col_num_sql2 = df.columns.get_loc(new_cols_arr[7])
            self.col_num_intent3 = df.columns.get_loc(new_cols_arr[8])
            self.col_num_sql3 = df.columns.get_loc(new_cols_arr[9])

def del_file(outputpath: str):
    if os.path.exists(outputpath):
        os.remove(outputpath)
        print(f"文件 {outputpath} 已删除。")
    else:
        print(f"文件 {outputpath} 不存在。")

def is_not_null(string):
    if string is None or string == "nan" or len(string.strip()) == 0:
        return False
    return True

def test_intent(field_en, field_cn, flag=''):
    if re.search(r'[a-zA-Z]', field_cn):
        index = re.search(r'[a-zA-Z]', field_cn).start()
        field_cn = field_cn[:index] if index > 1 else field_cn[:8]
    if flag == flagArr[0]:  
        return f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[1]:  
        return f"验证：目标表与源表迁移数据总数的一致性"
    elif flag in [flagArr[2], flagArr[4]]:  
        return f"验证：{field_en}({field_cn})取值的正确性"
    elif flag in [flagArr[3], flagArr[5]]:  
        return f"验证：{field_en}({field_cn})取值的正确性"
    elif flag == flagArr[6]:  
        return f"验证：主键不为空"
    elif flag == flagArr[7]:  
        return f"验证：目标表数据的唯一性"
    elif flag == flagArr[8]:  
        return f"验证：{field_en}({field_cn})码值在落标码值范围内"
    else:
        return ""

def str_is_null(tab_name, field, row_bean, field_not_null=True):
    if not is_not_null(row_bean[new_cols_arr[3]]):  
        str_sql = f"select count(1) as tcount from {tab_name} where nvl({field},'') !=''"
    elif is_not_null(row_bean[new_cols_arr[3]]) and not is_not_null(row_bean[new_cols_arr[2]]):  
        if field_not_null:
            str_sql = f"select count(1) as tcount from {tab_name} t1,{row_bean[new_cols_arr[1]]} t2 where {row_bean[new_cols_arr[3]]} and nvl({field},'') !='' "
        else:
            str_sql = f"select count(1) as tcount from {tab_name} t1,{row_bean[new_cols_arr[1]]} t2 where {row_bean[new_cols_arr[3]]}"
    elif is_not_null(row_bean[new_cols_arr[3]]) and is_not_null(row_bean[new_cols_arr[2]]):  
        if field_not_null:
            str_sql = f"select count(1) as tcount from {tab_name} t1,{row_bean[new_cols_arr[1]]} t2 where {row_bean[new_cols_arr[3]]} and nvl({field},'') =nvl({row_bean[new_cols_arr[2]]},'')"
        else:
            str_sql = f"select count(1) as tcount from {tab_name} t1,{row_bean[new_cols_arr[1]]} t2 where {row_bean[new_cols_arr[3]]} and t1.{field} =t2.{row_bean[new_cols_arr[2]]}"
    else:
        str_sql = f"select count(1) as tcount from {tab_name}"
    return str_sql

def primary_key_is_right():
    return ""

def primary_key_only():
    return ""

def tab_counts(row, tab_index=2):
    if tab_index in [0, 1]:
        return f"select count(1) as tcount from {row[new_cols_arr[tab_index]]}"
    elif tab_index == 2:
        return f"select 0 as tcount"
    else:
        return f"select '' as tcount"

# 读取 Excel 文件，获取所有sheets
df_all = pd.read_excel(FILE_URL_IN, sheet_name=None)
df_all.to_excel(FILE_URL_OUT, index=False)

# 创建容器，存储每个 sheet 的 DataFrame
sheets_data = {}
sheets_attr = {}

# 遍历每个 sheet,并存入字典中
for sheet_name in df_all.keys():
    sheets_data[sheet_name] = df_all[sheet_name]
    sheets_attr[sheet_name] = SheetBean(df_all[sheet_name])

for sheet in sheets_data:
    df = sheets_data[sheet]
    sbean = sheets_attr[sheet]

    # 总行数和总列数
    df_rows = df.shape[0]
    df_cols = df.shape[1]

    # 选择 0 到 最大 列,替换nan none 为"",并转换成字符串格式
    df = df.iloc[:, 0:df_cols].fillna("").astype(str)
    columnNameArr = ["字段名称", "中文名称", "字段类型", "可空", "", "备注"
        , "返回目录", "目标表名(t1)", "源表名(t2)", "原表字段", "关联关系"
        , "测试意图", "sql1", "sql2", "sql3"]
    for index, row in df.iterrows():
        if not sbean.is_table_sheet:
            break

        if row[old_cols_arr[5]] == PRIMARY_KEY:
            df.loc[index, df.columns[sbean.col_num_intent1]] = test_intent("", "", flagArr[6])
            df.loc[index, df.columns[sbean.col_num_sql1]] = str_is_null(row[new_cols_arr[7]], row[old_cols_arr[0]], row)
            df.loc[index, df.columns[sbean.col_num_sql2]] = tab_counts(row, 0)
        elif row[columnNameArr[3]] == flagArr[3] or row[columnNameArr[3]] == flagArr[5]:
            df.loc[index, df.columns[sbean.col_num_intent1]] = test_intent(row[old_cols_arr[0]], row[old_cols_arr[1]], flagArr[3])
            df.loc[index, df.columns[sbean.col_num_sql1]] = str_is_null(row[new_cols_arr[7]], row[old_cols_arr[0]], row)
            df.loc[index, df.columns[sbean.col_num_sql2]] = tab_counts(row, 0)
        elif row[columnNameArr[3]] == flagArr[2] or row[columnNameArr[3]] == flagArr[4]:
            df.loc[index, df.columns[sbean.col_num_intent1]] = test_intent(row[old_cols_arr[0]], row[old_cols_arr[1]], flagArr[2])
            df.loc[index, df.columns[sbean.col_num_sql1]] = str_is_null(row[new_cols_arr[7]], row[old_cols_arr[0]], row, False)
            df.loc[index, df.columns[sbean.col_num_sql2]] = tab_counts(row, 0)
        elif index == df_rows - 1:
            df.loc[index, df.columns[sbean.col_num_intent1]] = test_intent("", "", flagArr[1])
            df.loc[index, df.columns[sbean.col_num_sql1]] = tab_counts(row, 0)
            df.loc[index, df.columns[sbean.col_num_sql2]] = tab_counts(row, 1)

# 删除之前生成的文件，并重新生成文件
del_file(FILE_URL_OUT)
# 或者将所有的sheet页合并成一个文件但每个sheet页写入到文件的不同工作表中
with pd.ExcelWriter(FILE_URL_OUT, engine='xlsxwriter') as writer:
    for sheet_name, df_sheet in df_all.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
# df_all.to_excel(FILE_URL_OUT, index=False)

