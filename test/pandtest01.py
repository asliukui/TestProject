import pandas as pd
STRING_URL = r'C:\Users\asliu\Desktop\aaa.xlsx'
# 读取 Excel 文件
data = pd.read_excel(STRING_URL, sheet_name=None)

# 存储每个 sheet 的 DataFrame
sheets_data = {}

# 遍历每个 sheet
for sheet_name in data.keys():
    sheets_data[sheet_name] = data[sheet_name]

# 打印每个 sheet 的前 5 行数据
for sheet, df in sheets_data.items():
    print(f'Sheet: {sheet}')
    print(df.head(10))