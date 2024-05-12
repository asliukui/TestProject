import os
import sys

PRIMARY_KEY = "是"

# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 设置输出文件名，如果存在先就删除，文件打开状态无法删除
file_to_delete = "date_bk.xlsx"

# FILE_URL_IN = os.path.join(same_level_directory, "pls_迁出至新信投_mapping_0510.xlsx")
FILE_URL_IN = os.path.join(same_level_directory, "xintou02.xlsx")
FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)


# 根据传入参数,拼接文件路径
def get_sys_args():
    if len(sys.argv) > 1:
        print("传递的参数:", sys.argv)
        param = sys.argv[1]
        global FILE_URL_IN
        global FILE_URL_OUT
        FILE_URL_IN = os.path.join(same_level_directory, param)
        FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
        print("输入的文件路径为:", FILE_URL_IN)
        print("输出的文件路径为:", FILE_URL_OUT)
    else:
        print("没有传递参数")


def del_file():
    if os.path.exists(FILE_URL_OUT):
        print("文件：",file_to_delete," 要在关闭状态才能删除重建哦！！")
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

