import pandas as pd
import common

"""
执行脚本的环境配置
1.安装python
2.在安装完python后安装pandas：pip install pandas
3.在安装完python后安装openpyxl：pip install openpyxl
4.安装xlsxwriter：pip install xlsxwriter
阿里云仓库镜像，用于下载依赖包：http://mirrors.aliyun.com/pypi/simple/
"""
# 获取启动脚本时传入的参数
common.get_sys_args()
common.init_pd_config(pd)


# 空串校验
def isNotNUll(stri):
    if stri is None:
        return False
    elif stri == "nan":
        return False
    elif len(stri.strip()) == 0:
        return False
    else:
        return True


# 判定值不为空
def get_sql(tabName: str, felid: str, rowBean, field_not_null=True):
    if not isNotNUll(rowBean.loc[common.column_list[sbean.col_num_where]]):  # 无where条件
        str_sql = f"select count(1) as tcount from {tabName} where nvl({felid},'') !=''"
    elif isNotNUll(rowBean.loc[common.column_list[sbean.col_num_where]]) and isNotNUll(
            rowBean.loc[common.column_list[sbean.col_num_old_field]]) == False:  # where列非空，old_field 空
        if field_not_null:
            str_sql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[common.column_list[sbean.col_num_old_tab]]} t2 where {rowBean.loc[common.column_list[sbean.col_num_where]]} and nvl({felid},'') !='' "
        else:
            str_sql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[common.column_list[sbean.col_num_old_tab]]} t2 where {rowBean.loc[common.column_list[sbean.col_num_where]]}"
    elif isNotNUll(rowBean.loc[common.column_list[sbean.col_num_where]]) and isNotNUll(
            rowBean.loc[common.column_list[sbean.col_num_old_field]]) == True:  # where列非空，old_field 非空
        if field_not_null:
            str_sql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[common.column_list[sbean.col_num_old_tab]]} t2 where {rowBean.loc[common.column_list[sbean.col_num_where]]} and nvl({felid},'') =nvl({rowBean.loc[common.column_list[sbean.col_num_old_field]]},'')"
        else:
            str_sql = f"select count(1) as tcount from {tabName} t1,{rowBean.loc[common.column_list[sbean.col_num_old_tab]]} t2 where {rowBean.loc[common.column_list[sbean.col_num_where]]} and t1.{felid} =t2.{rowBean.loc[common.column_list[sbean.col_num_old_field]]}"
    else:
        str_sql = f"select count(1) as tcount from {tabName}"
    return str_sql


# 读取 Excel 文件，获取所有sheets
df_all = pd.read_excel(common.FILE_URL_IN, sheet_name=None)
# 创建容器，存储每个 sheet 的 DataFrame
sheets_data = {}
sheets_attr = {}
# 创建容器，存储每个 sheet 的属性。
# 遍历每个 sheet,并存入字典中
for sheet_name in df_all.keys():
    sheets_data[sheet_name] = df_all[sheet_name]
    sheets_attr[sheet_name] = common.SheetBean(df_all[sheet_name])
for sheet in sheets_data:
    df = sheets_data[sheet]
    sbean = sheets_attr[sheet]
    # sys.exit()
    # 总行数和总列数
    df_rows = df.shape[0]
    df_cols = df.shape[1]
    # 选择 0 到 最大 列,替换nan none 为"",并转换成字符串格式
    df = df.iloc[:, 0:df_cols].fillna("").astype(str)

    for index, row in df.iterrows():
        if not sbean.is_table_sheet:
            break
        if row[common.column_list[sbean.col_num_field_remark]] == common.PRIMARY_KEY:  # 1.主键不为空;2.执行语句
            df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent("", "", common.flagArr[6])  #
            df.loc[index, df.columns[sbean.col_num_sql1]] = get_sql(row.iloc[7], row.iloc[0],
                                                                    row)  # 测试意图,主键
            df.loc[index, df.columns[sbean.col_num_sql2]] = common.get_tab_tcount(row, sbean, sbean.col_num_new_tab)
        elif row[common.column_list[sbean.col_num_field_isnull]] == common.flagArr[3] or row[
            common.column_list[sbean.col_num_field_isnull]] == common.flagArr[5]:  # 1.测试意图,判断非主键，不可为空 2.执行sql语句
            df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent(row.iloc[0], row.iloc[1],
                                                                                  common.flagArr[3])
            df.loc[index, df.columns[sbean.col_num_sql1]] = get_sql(row.iloc[7], row.iloc[0],
                                                                    row)  # sql判定值不为空
            df.loc[index, df.columns[sbean.col_num_sql2]] = common.get_tab_tcount(row, sbean,
                                                                                  sbean.col_num_new_tab)  # 验证sql2
        elif row[common.column_list[sbean.col_num_field_isnull]] == common.flagArr[2] or row[
            common.column_list[sbean.col_num_field_isnull]] == common.flagArr[4]:  # 1.测试意图,判断非主键，可空 2.执行sql语句
            df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent(row.iloc[0], row.iloc[1],
                                                                                  common.flagArr[2])
            df.loc[index, df.columns[sbean.col_num_sql1]] = get_sql(row.iloc[7], row.iloc[0],
                                                                    row, False)  # sql判定值不为空
            df.loc[index, df.columns[sbean.col_num_sql2]] = common.get_tab_tcount(row, sbean,
                                                                                  sbean.col_num_new_tab)  # 验证sql2
        elif index == df_rows - 1:  # 1.测试意图,统计table数据总量 2.执行sql语句
            df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent("", "",
                                                                                  common.flagArr[1])
            df.loc[index, df.columns[sbean.col_num_sql1]] = common.get_tab_tcount(row, sbean, sbean.col_num_new_tab)
            df.loc[index, df.columns[sbean.col_num_sql2]] = common.get_tab_tcount(row, sbean, sbean.col_num_old_tab)
    # 将修改后的 df 写回到 df_all 中对应的 sheet 中
    df_all[sheet] = df

# 删除之前是生成的文件，并重新生成文件
common.del_file()
# 将所有的sheet页合并成一个文件但每个sheet页写入到文件的不同工作表中
with pd.ExcelWriter(common.FILE_URL_OUT, engine='xlsxwriter') as writer:
    for sheet_name, df_sheet in df_all.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
