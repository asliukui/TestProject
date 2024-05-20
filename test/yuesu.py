import re

import pandas as pd
from pandas import DataFrame
import common

file_path = "/Users/lk/ProjectRes/PycharmProjects/TestProject/test/yusu.xlsx"

col_name = ['页名', '新表名', '新表字段', '测试意图','新表中文名', '源表名', '源表字段', '约束描述', '约束sql', "录入预制选项"]
FILE_URL_OUT = "/Users/lk/ProjectRes/PycharmProjects/TestProject/test/ys_out.xlsx"
df_all = pd.read_excel(common.FILE_URL_IN, sheet_name=None)
# 创建另一个 df_all的类型
# 创建容器，存储每个 sheet 的 DataFrame
sheets_data = {}
# 创建容器，存储每个 sheet 的属性。
# 遍历每个 sheet,并存入字典中
# 初始化约束表
ydf = pd.read_excel(file_path, sheet_name='技术规则')
ndf = pd.DataFrame(columns=col_name)
for sheet_name in df_all.keys():
    if (sheet_name == "目录") or ("Sheet" in sheet_name):
        continue
    df = df_all[sheet_name]
    sheets_data[sheet_name] = df

ndf_index = 2
for sheet in sheets_data:
    sdf = sheets_data[sheet]
    if len(sdf.columns) < 48:
        continue
    if re.match(r'[a-zA-Z]', sdf.columns[1][0]):
        tab_en = str(sdf.columns[1])
        tab_cn = str(sdf.iloc[0, 1])
        tab_en_cn = str(sdf.columns[1]) + "-" + str(sdf.iloc[0, 1])
    else:
        tab_en = str(sdf.iloc[0, 1])
        tab_cn = str(sdf.columns[1])
        tab_en_cn = str(sdf.iloc[0, 1]) + "-" + str(sdf.columns[1])
    for index, row in enumerate(sdf.iterrows()):
        if index <= 2: continue
        if not sdf.iloc[5:, 26].isnull().all():

            if '.' in str(sdf.iloc[index, 28]):
                flied_s_en = str(sdf.iloc[index, 28]).split('.')[1]
            else:
                flied_s_en = sdf.iloc[index, 28]
            s_tab_name = str(sdf.iloc[index, 26]).lower()
            for i, rs in enumerate(ydf.iterrows()):
                if i <= 1:
                    continue
                y_tab_name = str(ydf.iloc[i, 7]).lower()
                y_flied_name = str(ydf.iloc[i, 9]).lower()
                if s_tab_name == y_tab_name and str(flied_s_en).lower() == str(y_flied_name).lower():
                    ndf.loc[ndf_index, '页名'] = sheet
                    ndf.loc[ndf_index, col_name[1]] = tab_en
                    ndf.loc[ndf_index, col_name[2]] = sdf.iloc[index, 1]
                    # 验证: 合同起始日(CTR_BGN_DT)
                    # 国内信用证开立，信用证兑付类型为即期时，信用证有效期必须与开证日相等
                    ndf.loc[ndf_index, col_name[3]] = "验证: " + str(sdf.iloc[index, 2]) + "(" + str(sdf.iloc[index, 1]) + ")"+str(ydf.iloc[i, 4])
                    ndf.loc[ndf_index, col_name[4]] = str(tab_en)+'-'+str(tab_cn)
                    ndf.loc[ndf_index, col_name[5]] = sdf.iloc[index, 26]
                    ndf.loc[ndf_index, col_name[6]] = flied_s_en
                    ndf.loc[ndf_index, col_name[7]] = ydf.iloc[i, 4]
                    ndf.loc[ndf_index, col_name[8]] = ydf.iloc[i, 13]
                    ndf.loc[ndf_index, col_name[9]] = ydf.iloc[i, 3]
                    ndf_index += 1
ndf.to_excel(FILE_URL_OUT, index=False)
# with pd.ExcelWriter(FILE_URL_OUT, engine='xlsxwriter') as writer:
#     for sheet_name, df_sheet in ndf.items():
#         df_sheet.to_excel(writer, sheet_name='约束过滤', index=False)
print("生成文件成功：" + FILE_URL_OUT)
