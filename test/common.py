import os
import sys
import re

# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 指定要删除的文件名
file_to_delete = "date_bk.xlsx"

# 默认文件路径用于测试代码
FILE_URL_IN = r'C:\Users\asliu\Desktop\aaa.xlsx'
FILE_URL_OUT = r"C:\Users\asliu\Desktop\a_bk.xlsx"

FILE_URL_IN = os.path.join(same_level_directory, "xintou02.xlsx")
FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
# 根据传入参数,拼接文件路径
def get_sys_args():
    if len(sys.argv) > 1:
        print("传递的参数:", sys.argv)
        param = sys.argv[1]
        FILE_URL_IN = os.path.join(same_level_directory, param)
        FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
    else:
        print("没有传递参数")


def del_file():
    if os.path.exists(FILE_URL_OUT):
        # 如果文件存在，则删除它
        os.remove(FILE_URL_OUT)
        print(f"文件 {FILE_URL_OUT} 已删除。")
    else:
        print(f"文件 {FILE_URL_OUT} 不存在。")


def init_pd_config(pd):
    # 设置显示完整的列
    pd.set_option('display.max_columns', None)
    # 设置显示完整的行
    pd.set_option('display.max_rows', None)
    pd.options.mode.copy_on_write = True
    return pd


column_list = ["字段名称", "中文名称", "字段类型", "可空", "", "备注"
    , "返回目录", "new_tab", "old_tab", "old_field", "where"
    , "intent1", "sql1", "intent2", "sql2", "intent3", "sql3"]
flagArr = ["主键", "sum", "YES", "NO", "是", "否", "主键不空", "主键唯一", "码值","字段取值比对"]
PRIMARY_KEY = "是"


# # 列值索引
# tit_str_index = {"字段名称": 0
#     , "中文名称": 1
#     , "字段类型": 2
#     , "可空": 3
#     , "mid_asset_iou_info_total": 4
#     , "备注": 5
#     , "返回目录": 6
#     , "new_tab": 7
#     , "old_tab": 8
#     , "old_field": 9
#     , "where": 10
#     , "intent1": 11
#     , "sql1": 12
#     , "intent2": 13
#     , "sql2": 14
#     , "intent3": 15
#     , "sql3": 16}
# #   键值互换的map {0: '字段名称', 1: '中文名称'...}
# tit_index_str = {value: key for key, value in tit_str_index.items()}


class SheetBean:

    def __init__(self, df):
        self.is_table_sheet = False
        self.columns_arr = []
        if len(df.columns) > 4:
            column_list[4] = df.columns[4]
        for column in df.columns:
            self.columns_arr.append(column)
            if check_array(column_list, self.columns_arr):
                self.is_table_sheet = True
            if column == column_list[0]:
                self.col_num_field_en = df.columns.get_loc(column)
            elif column == column_list[1]:
                self.col_num_field_cn = df.columns.get_loc(column)
            elif column == column_list[2]:
                self.col_num_field_type = df.columns.get_loc(column)
            elif column == column_list[3]:
                self.col_num_field_isnull = df.columns.get_loc(column)
            elif column == column_list[4]:
                self.col_num_field_mid_tab = df.columns.get_loc(column)
            elif column == column_list[5]:
                self.col_num_field_remark = df.columns.get_loc(column)
            elif column == column_list[6]:
                self.col_num_field_bk = df.columns.get_loc(column)
            elif column == column_list[7]:
                self.col_num_new_tab = df.columns.get_loc(column)
            elif column == column_list[8]:
                self.col_num_old_tab = df.columns.get_loc(column)
            elif column == column_list[9]:
                self.col_num_old_field = df.columns.get_loc(column)
            elif column == column_list[10]:
                self.col_num_where = df.columns.get_loc(column)
            elif column == column_list[11]:
                self.col_num_intent1 = df.columns.get_loc(column)
            elif column == column_list[12]:
                self.col_num_sql1 = df.columns.get_loc(column)
            elif column == column_list[13]:
                self.col_num_intent2 = df.columns.get_loc(column)
            elif column == column_list[14]:
                self.col_num_sql2 = df.columns.get_loc(column)
            elif column == column_list[15]:
                self.col_num_intent3 = df.columns.get_loc(column)
            elif column == column_list[16]:
                self.col_num_sql3 = df.columns.get_loc(column)


def check_array(array1, columns_arr):
    for element in array1:
        if element not in columns_arr:
            # print(f"缺少列名：{element}")
            return False
    return True


# 测试意图,字段英文名，中文名，标示
def test_intent(field_en: str, field_cn: str, flag=''):
    # if re.search(r'[a-zA-Z]', field_cn):
    #     index = re.search(r'[a-zA-Z]', field_cn).start()
    #     if index > 1:
    #         field_cn = field_cn[:index]
    #     else:
    #         field_cn = field_cn[:8]
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
    elif flag == flagArr[9]:  # 字段取值比对
        strlog = f"验证：{field_en}({field_cn})取值的正确性"
    else:
        strlog = ""
    return strlog


# 总条数,tab_index: {0:new_tab , 1-old_tab , 2-select 0 , 3-select ''}
def get_tab_tcount(row, sbean, tab_index=2):
    if tab_index in [sbean.col_num_new_tab, sbean.col_num_old_tab]:
        return f"select count(1) as tcount from {row[column_list[tab_index]]}"
    elif tab_index == 2:
        return f"select 0 as tcount from dual"
    else:
        return f"select '' as tcount from dual"
