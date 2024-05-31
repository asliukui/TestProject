import os

import pandas as pd

FILE_NAME_L = "date_bk_l.xlsx"
FILE_NAME_P = "date_bk_p.xlsx"
FILE_NAME_S = "date_bk_s.xlsx"
# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)

FILE_URL_IN_L = os.path.join(same_level_directory, "L_XT_code_mapping_1.xlsx")
FILE_URL_IN_P = os.path.join(same_level_directory, "P_XT_code_mapping_1.xlsx")

FILE_URL_OUT_L = os.path.join(same_level_directory, "function_xt_l.sql")
FILE_URL_OUT_P = os.path.join(same_level_directory, "function_xt_p.sql")
FILE_URL_OUT_S = os.path.join(same_level_directory, "function_xt_s.sql")


def del_file(file_path):
    if os.path.exists(file_path):
        # 如果文件存在，则删除它
        os.remove(file_path)
        print(f"文件 {file_path} 已删除。")
    else:
        print(f"文件 {file_path} 不存在。")


del_file(FILE_URL_OUT_L)
del_file(FILE_URL_OUT_P)


df_L = pd.read_excel(FILE_URL_IN_L, sheet_name='Sheet1')
df_P = pd.read_excel(FILE_URL_IN_P, sheet_name='Sheet1')
# 去重
function_list = df_L['CodeNo'].drop_duplicates().values
# L 行信投逻辑
# 遍历标识，取每一行码值拼接
for index, name in enumerate(function_list):
    if name is None or name == 'nan' or name == 'NAN' or name == '':
        continue
    selected_rows = df_L[df_L["CodeNo"] == name]
    creat_fun_sql = ""
    for i, row in enumerate(selected_rows.itertuples()):
        Code1str = "NULL" if row.Code1 is None or len(str(row.Code1)) == 0 or str(row.Code1) == 'nan' or str(
            row.Code1) == ' ' else f"\'{row.Code1}\'"
        Code2str = "NULL" if row.Code2 is None or len(str(row.Code2)) == 0 or str(row.Code2) == 'nan' or str(
            row.Code2) == ' ' else f"\'{row.Code2}\'"
        if i == 0:
            creat_fun_sql = (f"CREATE OR REPLACE FUNCTION {name}_ZDJX(CODE VARCHAR(30)) \n"
                             f"RETURNS VARCHAR(30) \n"
                             f"LANGUAGE SQL \n"
                             f"BEGIN \n"
                             f"RETURN DECODE(TRIM(CODE)\n,{Code1str},{Code2str} \n")
        else:
            creat_fun_sql += f",{Code1str},{Code2str}\n"
        # 获取row行第二列的值
        if len(selected_rows) - 1 == i:
            creat_fun_sql += (f",CODE ); \n"
                              f"END; \n\n\n")

    # 将sql写入文件
    with open(FILE_URL_OUT_L, 'a', encoding='utf-8') as f:
        f.write(creat_fun_sql)


