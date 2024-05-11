import pandas as pd
import common
import Bean

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


# noinspection SqlResolve
def get_tab_tcount(tab_index=4):
    if tab_index == 0:  # 查自己
        return f"select count(1) as tcount from table_tar "
    elif tab_index == 1:  # 1张中间表 统计数据量
        return f"select count(1) as tcount from tableA "
    elif tab_index == 2:  # 2张中间表
        return (f"select sum(tcount) as tcount from ("
                f"select count(1) as tcount from tableA "
                f" union  all "
                f"select count(1) as tcount from tableB)")
    elif tab_index == 3:  # 3张中间表
        return (f"select sum(tcount) as tcount from ("
                f"select count(1) as tcount from tableA "
                f" union  all "
                f"select count(1) as tcount from tableB "
                f" union  all "
                f"select count(1) as tcount from tableC)")
    elif tab_index == 4:
        return f"select 0 as tcount from dual"
    else:
        return f"select '' as tcount from dual"


def get_field_true(index, row, df, tab_index=4):
    if tab_index == 0:  # 查自己
        return f"select count(1) as tcount from table_tar where nvl({df.iloc[0, 1]},'') !=''"
    elif tab_index == 1:  # 1张中间表 统计数据量
        if index == 0:
            return f"select count(1) as tcount from table_tar t,(select {df.iloc[0, 20].replace(',', '')} from tableA ) a where  nvl(t.{row.iloc[1]},'') = nvl(a.{row.iloc[16].replace(',', '')},'') "
        else:
            return f"select count(1) as tcount from table_tar t,(select {df.iloc[0, 20].replace(',', '')},{row.iloc[20].replace(',', '')} from tableA ) a where t.{df.iloc[0, 1]} = nvl(a.{df.iloc[0, 16].replace(',', '')},'') and nvl(t.{row.iloc[1]},'') = nvl(a.{row.iloc[16].replace(',', '')},'') "
    elif tab_index == 2:  # 2张中间表
        if index == 0:
            return (f"select count(1) as tcount from table_tar t,("
                    f"select {df.iloc[0, 20].replace(',', '')} from tableA "
                    f" union  all "
                    f"select {df.iloc[0, 20].replace(',', '')} from tableB) a where  t.{row.iloc[1]} = nvl(a.{row.iloc[16].replace(',', '')},'')")
        else:
            return (f"select count(1) as tcount from table_tar t,("
                    f"select {df.iloc[0, 20].replace(',', '')},{row.iloc[20].replace(',', '')} from tableA "
                    f" union  all "
                    f"select {df.iloc[0, 20].replace(',', '')},{row.iloc[20].replace(',', '')} from tableB) a where t.{df.iloc[0, 1]} = nvl(a.{df.iloc[0, 16].replace(',', '')},'') and t.{row.iloc[1]} = nvl(a.{row.iloc[16].replace(',', '')},'')")
    elif tab_index == 3:  # 3张中间表
        if index == 0:
            return (f"select count(1) as tcount from table_tar t ,("
                    f"select {row.iloc[16].replace(',', '')} from tableA "
                    f" union  all "
                    f"select {row.iloc[16].replace(',', '')} from tableB"
                    f" union  all "
                    f"select {row.iloc[16].replace(',', '')} from tableC) a "
                    f"where t.{row.iloc[1]} = nvl(a.{row.iloc[16].replace(',', '')},'')")
        else:
            return (f"select count(1) as tcount from table_tar t ,("
                    f"select {df.iloc[0, 16].replace(',', '')},{row.iloc[16].replace(',', '')} from tableA "
                    f" union  all "
                    f"select {df.iloc[0, 30].replace(',', '')},{row.iloc[30].replace(',', '')} from tableB "
                    f" union  all "
                    f"select {df.iloc[0, 41].replace(',', '')},{row.iloc[41].replace(',', '')} from tableC) a "
                    f"where t.{df.iloc[0, 1]} = a.{df.iloc[0, 16].replace(',', '')} and t.{row.iloc[1]} = nvl(a.{row.iloc[16].replace(',', '')},'')")
    elif tab_index == 4:
        return f"select 0 as tcount from dual"
    else:
        return f"select '' as tcount from dual"


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
    if sheet_name == "目录":
        continue
    df = df_all[sheet_name]

    # 定义要添加的列名和对应的值
    # new_columns = ["intent1", "sql1", "intent2", "sql2", "intent3", "sql3"]
    # new_values = ["intent1", "sql1", "intent2", "sql2", "intent3", "sql3"]

    new_columns = ["intent1", "sql1", "intent2", "sql2", "intent3", "sql3"]
    # 使用 assign 方法批量添加空列
    df = df.assign(**{column: None for column in new_columns})

    sheets_data[sheet_name] = df
    sheets_attr[sheet_name] = common.SheetBean(df)
for sheet in sheets_data:

    df = sheets_data[sheet]

    # df = df.drop([0, 1])
    # df.columns = df.iloc[0]

    # print(df.columns)
    sbean = sheets_attr[sheet]
    # sys.exit()
    # 总行数和总列数
    # print(df.shape)
    df_rows = df.shape[0]
    df_cols = df.shape[1]
    # 选择 0 到 最大 列,替换nan none 为"",并转换成字符串格式
    # df = df.iloc[:, 0:df_cols].fillna("").astype(str)
    mainList = []
    mapList_1 = []
    mapList_2 = []
    mapList_3 = []
    # 表主键集合
    primaryKeyList = []
    # 初始化：目标表实体类集合
    for index, row in df.iterrows():
        # 通过行号获取行数据，初始化Bean.MainBean,并存入mainList。mainBean初始化的第一个参数是 df.columns[1],从第二个参数开始依次是df.iloc[index,1]到df.iloc[index,12]。
        if index <= 2: continue
        mainList.append(
            Bean.MainBean(df.columns[1], df.iloc[index, 0], df.iloc[index, 1], df.iloc[index, 2], df.iloc[index, 3],
                          df.iloc[index, 4], df.iloc[index, 5], df.iloc[index, 6], df.iloc[index, 7], df.iloc[index, 8],
                          df.iloc[index, 9], df.iloc[index, 10], df.iloc[index, 11], df.iloc[index, 12]))
        # 根据df.iloc[index, 5]判断是否为主键，若 df.iloc[index, 4] = '是' ,则df.iloc[index, 1]存入primaryKeyList,配上自增序号
        if df.iloc[index, 4] == common.PRIMARY_KEY:
            primaryKeyList.append(index)
        # 初始化mapBean,根据'原表字段英文名'列判断，都为空则该系统映射，否则有字段映射
        # 用pandas判断16列第5行以后的值是否为都空，第一段系统
        if df.iloc[5:, 14].isnull().all():
            print("16列第5行以后的值都为空，源表英文字段名")
        else:
            # 初始化Bean.MapBean,并存入mapList1。mapbean初始化的参数从13开始到24，df.iloc[index,13]
            mapList_1.append(
                Bean.MapBean(df.iloc[index, 13], df.iloc[index, 14], df.iloc[index, 15], df.iloc[index, 16],
                             df.iloc[index, 17], df.iloc[index, 18], df.iloc[index, 19], df.iloc[index, 20],
                             df.iloc[index, 21], df.iloc[index, 22], df.iloc[index, 23], df.iloc[index, 24]))
        if df.iloc[5:, 26].isnull().all():
            print("16列第5行以后的值都为空")
        else:
            # 初始化Bean.MapBean,并存入mapList2。mapbean初始化的参数从25开始到36，df.iloc[index,25]
            mapList_2.append(
                Bean.MapBean(df.iloc[index, 25], df.iloc[index, 26], df.iloc[index, 27], df.iloc[index, 28],
                             df.iloc[index, 29], df.iloc[index, 30], df.iloc[index, 31], df.iloc[index, 32],
                             df.iloc[index, 33], df.iloc[index, 34], df.iloc[index, 35], df.iloc[index, 36]))
        if df.iloc[5:, 38].isnull().all():
            print("16列第5行以后的值都为空")
        else:
            print(df.iloc[5:, 38].isnull().all())
            print(df.iloc[5:, 38])
            # 初始化Bean.MapBean,并存入mapList3。mapbean初始化的参数从37开始到48，df.iloc[index,37]
            mapList_3.append(
                Bean.MapBean(df.iloc[index, 37], df.iloc[index, 38], df.iloc[index, 39], df.iloc[index, 40],
                             df.iloc[index, 41], df.iloc[index, 42], df.iloc[index, 43], df.iloc[index, 44],
                             df.iloc[index, 45], df.iloc[index, 46], df.iloc[index, 47], df.iloc[index, 48]))

    # 生成新列名‘字段取值的正确性’
    df['字段取值的正确性'] = None
    # 生成新列名‘正确性验证sql’
    df['正确性验证sql'] = None
    # 获取这两列的索引 '字段取值的正确性','正确性验证sql'
    col_num_ver_field = df.columns.get_loc('字段取值的正确性')
    col_num_ver_sql = df.columns.get_loc('正确性验证sql')
    # 对len1 赋值，当 len(mapList_1) > 0 赋值1，否则赋值0
    len1 = 1 if len(mapList_1) > 0 else 0
    len2 = 1 if len(mapList_2) > 0 else 0
    len3 = 1 if len(mapList_3) > 0 else 0
    # 打印maplist3的内容
    for i in range(len(mapList_3)):
        print(mapList_3[i].source_table_en)
    # '字段取值的正确性','正确性验证sql'
    for index, row in df.iterrows():
        if index < 3:
            continue
        # if df.iloc[index, 4] == common.PRIMARY_KEY or (df.iloc[index, 4] == "Y"):
        df.loc[index, df.columns[
            col_num_ver_field]] = f"验证：{mainList[index - 3].field_cn}({mainList[index - 3].field_en})取值的正确性"
        sql1 = f"select count (1) as tcount from {mainList[index - 3].table_name} as t, ( "
        if len1 > 0:
            templist = mapList_1
            # sql1+= f"\n select {}"
            # sql1 += f"{templist[index - 3].source_table_en} as t1 where "
            # 遍历primarykeyList,拼接sql
            sql1 += f"\n select "
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                sql1 += f" {templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                     f"from tableA \n")

        if len2 > 0:
            templist = mapList_2
            sql1 += f"union all \n select "
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                sql1 += f" {templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                     f"from tableB \n")

        if len3 > 0:
            templist = mapList_3
            sql1 += f"union all \n select "
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                sql1 += f" {templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                     f"from tableC \n")
        # sql 拼接主键的关联
        for i in range(len(primaryKeyList)):
            if i > 0:
                sql1 += 'and '
            sql1 += f") t1 \nwhere t. {mainList[primaryKeyList[i] - 3].field_en} = t1.{mainList[primaryKeyList[i] - 3].field_en} \n"
        if mainList[index - 3].is_primary_key != common.PRIMARY_KEY:
            sql1 += f" and nvl(t.{mainList[index - 3].field_en},'') = nvl(t1.{mainList[index - 3].field_en}) \n"
        df.loc[index, df.columns[col_num_ver_sql]] = sql1
    # clumns_isnull = []
    # for index, row in df.iterrows():
    #     if index < 3:
    #         continue
    #
    #     if index == 0:
    #         # 定义数组，用于存储不可为空值的字段名称
    #         clumns_isnull = []
    #     # print(df.iloc[0, 20])
    #     if df.iloc[index, 4] == common.PRIMARY_KEY or (df.iloc[index, 4] == "Y"):  # 1.主键唯一;2.执行语句
    #         df.loc[df_rows + 1, df.columns[sbean.col_num_intent1]] = common.test_intent("", "", common.flagArr[7])  #
    #         df.loc[df_rows + 1, df.columns[
    #             sbean.col_num_sql1]] = f"select count (1) as tcount from (select count (1) as tcount from table_tar where nvl({df.iloc[index, 1]},'') !='' group by {df.iloc[index, 1]}) "
    #         df.loc[df_rows + 1, df.columns[sbean.col_num_sql2]] = get_tab_tcount(0)
    #     if (df.iloc[index, 5] == "否") or (df.iloc[index, 5] == "N"):  # 1.测试意图,判断非主键，不可为空 2.执行sql语句
    #         if isNotNUll(df.iloc[index, 1]):
    #             clumns_isnull.append(df.iloc[index, 1])  # 存储不可为空值的字段名称，在最后一行进行打印
    #         # df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent(row.iloc[2], row.iloc[1],
    #         #                                                                       common.flagArr[3])
    #         # df.loc[index, df.columns[
    #         #     sbean.col_num_sql1]] = f"select count(1) as tcount from table_tar where nvl({df.iloc[index, 1]},'') !=''"  # sql判定值不为空
    #         # df.loc[index, df.columns[sbean.col_num_sql2]] = get_tab_tcount(0)
    #     if isNotNUll(df.iloc[index, 8]):  # 码值,码值在落标码值范围内
    #         df.loc[index, df.columns[sbean.col_num_intent1]] = common.test_intent(row.iloc[2], row.iloc[1],
    #                                                                               common.flagArr[8])
    #         in_code = df.iloc[index, 8]
    #         result = [i.split('-')[0] for i in in_code.split()]
    #         result = str(result).replace('[', "(")
    #         result = str(result).replace(']', ")")
    #         # print(str(result))
    #         df.loc[index, df.columns[
    #             sbean.col_num_sql1]] = f"select count(1) as tcount from table_tar where {df.iloc[index, 1]} not in {result}"
    #     # print(df.iloc[index,8])
    #     # 验证数据的准确性
    #     df.loc[index, df.columns[sbean.col_num_intent3]] = common.test_intent(row.iloc[2], row.iloc[1],
    #                                                                           common.flagArr[9])
    #     if sbean.col_num_intent1 in [25, 26]:  # 3段映射
    #         df.loc[index, df.columns[sbean.col_num_sql3]] = get_field_true(index, row, df, 1)
    #     elif sbean.col_num_intent1 == 37:
    #         df.loc[index, df.columns[sbean.col_num_sql3]] = get_field_true(index, row, df, 2)
    #     elif sbean.col_num_intent1 == 49:
    #         df.loc[index, df.columns[sbean.col_num_sql3]] = get_field_true(index, row, df, 3)
    #
    #     # 1.测试意图,统计table数据总量 2.执行sql语句
    #     if index == df_rows - 1:
    #         df.loc[index + 1, df.columns[sbean.col_num_intent1]] = common.test_intent("", "",
    #                                                                                   common.flagArr[1])
    #         df.loc[index, df.columns[sbean.col_num_sql1]] = get_tab_tcount(0)
    #         if sbean.col_num_intent1 == 25:  # 3段映射
    #             df.loc[index + 1, df.columns[sbean.col_num_sql2]] = get_tab_tcount(1)
    #         elif sbean.col_num_intent1 == 37:
    #             df.loc[index + 1, df.columns[sbean.col_num_sql2]] = get_tab_tcount(2)
    #         elif sbean.col_num_intent1 == 49:
    #             df.loc[index + 1, df.columns[sbean.col_num_sql2]] = get_tab_tcount(3)
    #         # 判断空字符串
    #         isnull_sql1 = ""
    #         isnull_sql2 = ""
    #         for i, clo_name in enumerate(clumns_isnull):
    #             if i == 0:
    #                 isnull_sql1 = f"select sum(case when nvl({clo_name}, '') = '' then 1 else 0 end) as {clo_name} "
    #                 isnull_sql2 = f"select 0 as {clo_name} "
    #             elif i == len(clumns_isnull) - 1:
    #                 isnull_sql1 = isnull_sql1 + f"\n,sum(case when nvl({clo_name}, '') = '' then 1 else 0 end) as {clo_name} \nfrom table_tar"
    #                 isnull_sql2 = isnull_sql2 + f"\n,0 as {clo_name} from dual"
    #             else:
    #                 isnull_sql1 = isnull_sql1 + f"\n,sum(case when nvl({clo_name}, '') = '' then 1 else 0 end) as {clo_name} "
    #                 isnull_sql2 = isnull_sql2 + f"\n,0 as {clo_name} "
    #         df.loc[index + 3, df.columns[sbean.col_num_intent1]] = "验证：必输项不可为空"
    #         df.loc[index + 3, df.columns[sbean.col_num_sql1]] = isnull_sql1
    #         df.loc[index + 3, df.columns[sbean.col_num_sql2]] = isnull_sql2
    #         df_all[sheet] = df

        # 将修改后的 df 写回到 df_all 中对应的 sheet 中
    df_all[sheet] = df

# 删除之前是生成的文件，并重新生成文件
common.del_file()
# 将所有的sheet页合并成一个文件但每个sheet页写入到文件的不同工作表中
with pd.ExcelWriter(common.FILE_URL_OUT, engine='xlsxwriter') as writer:
    for sheet_name, df_sheet in df_all.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
