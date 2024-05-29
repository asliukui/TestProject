import os

import pandas as pd

FILE_NAME_L = "date_bk_l.xlsx"
FILE_NAME_P = "date_bk_p.xlsx"
FILE_NAME_S = "date_bk_s.xlsx"
# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 设置输出文件名，如果存在先就删除，文件打开状态无法删除

out_file = "function_sc.sql"
# FILE_URL_IN = os.path.join(same_level_directory, "xintou_dev.xlsx")
FILE_URL_IN = os.path.join(same_level_directory, "L_XT_code_mapping_1.xlsx")
FILE_URL_OUT = os.path.join(same_level_directory, out_file)


df = pd.read_excel(FILE_URL_IN, sheet_name='Sheet1')
"Index(['CodeNo', 'Code1', 'Note1', 'CodeNo2', 'Code2', 'Note2', 'Unnamed: 6'], dtype='object')"
# 去重
function_list = df['CodeNo'].drop_duplicates().values
#L 行信投逻辑
#遍历标识，取每一行码值拼接
for index, name in enumerate(function_list):
    selected_rows = df[df['CodeNo'] == name]
    for row_index , row in enumerate(selected_rows.iterrows()) :
        print(row['Code1'])
        combined_value = row['B'] + row['D']
        if row_index == 0 :
            creat_fun_sql = (f"CREATE OR REPLACE FUNCTION {name}_ZDJX(CODE VARCHAR(30)) \n"
                             f"RETURNS VARCHAR(30) \n"
                             f"LANGUAGE SQL \n"
                             f"BEGIN \n"
                             f"RETURN DECODE(TRIM(CODE),{row['Code1']},{row['Code1']} \n)")
        #获取row行第二列的值

            print(row)




# selected_rows = df[df['CodeNo'] == 444]
# print(selected_rows)
print(df.columns)