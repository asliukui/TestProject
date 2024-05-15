import re
from typing import Dict, Any

import pandas as pd
import common
import Bean

"""
执行脚本的环境配置
1.安装python
2.在安装完python后安装pandas：pip install pandas
3.在安装完python后安装openpyxl：pip install openpyxl
4.安装xlsxwriter：pip install xlsxwriter
#可忽略：阿里云仓库镜像，用于下载依赖包：http://mirrors.aliyun.com/pypi/simple/
5.执行脚本
5.1.将mapping文件放入xintou02.py同文件夹内
5.2.执行脚本：python xintou02.py 你的文件名称.xlsx，根据你安装的python版本选择执行命令
如:python xintou02.py "SCB_新一代新信投项目群_新信投系统中间表数据据映射mapping-V0.01(pls迁出至新信投) -规则情况统计_20240511.xlsx"
如:python3 xintou02.py "SCB_新一代新信投项目群_新信投系统中间表数据据映射mapping-V0.01(pls迁出至新信投) -规则情况统计_20240511.xlsx"
6.输出文件为：date_bk.xlsx，在xintou02.py同文件夹内
"""

#开关，信投映射在字段英文名列-False，映射在映射规则-True
MAPPING_KEY = False
# 获取启动脚本时传入的参数
common.get_sys_args()
common.init_pd_config(pd)

# 读取 Excel 文件，获取所有sheets，'None'表示读取所有的sheet，可以换成单个sheet名
# df_all = pd.read_excel(common.FILE_URL_IN, sheet_name="贷款申请信息-借据列表")
df_all = pd.read_excel(common.FILE_URL_IN, sheet_name=None)
# 创建另一个 df_all的类型
df_all2: Dict[Any, pd.DataFrame] = {}
# 创建容器，存储每个 sheet 的 DataFrame
sheets_data = {}
# 创建容器，存储每个 sheet 的属性。
# 遍历每个 sheet,并存入字典中
for sheet_name in df_all.keys():
    if (sheet_name == "目录") or ("Sheet" in sheet_name):
        continue
    df = df_all[sheet_name]
    sheets_data[sheet_name] = df

#  计数器，显示处理进度，提高脚本等待的体验。
count_num = 0
for sheet in sheets_data:
    count_num += 1
    print(len(sheets_data) - count_num, sheet)

    ndf = pd.DataFrame(columns=common.test_file_clos)
    ndf.loc[1] = common.test_file_des

    df = sheets_data[sheet]

    # sys.exit()
    # 总行数和总列数
    df_rows = df.shape[0]
    df_cols = df.shape[1]
    # 选择 0 到 最大 列,替换nan none 为"",并转换成字符串格式
    # df = df.iloc[:, 0:df_cols].fillna("").astype(str)
    mainList = []
    mapList_1 = []
    mapList_2 = []
    mapList_3 = []
    # L = df.iloc[0, 13][0]
    # P = df.iloc[0, 25][0]
    # S = df.iloc[0, 37][0]
    # 表主键集合
    primaryKeyList = []
    table_catch1 = ""
    table_catch2 = ""
    table_catch3 = ""
    # 第一列不为空的行数
    col0_count = (df.iloc[:, 0].notnull()).sum()
    if MAPPING_KEY:
        if not df.iloc[5:, 20].isnull().all():
            # 去除第16列的空值
            # table_catch1 = df.iloc[:, 20].dropna().iloc[-1]
            table_catch1=df.iloc[col0_count, 20] if col0_count < df_rows else None
        if not df.iloc[5:, 32].isnull().all():
            table_catch2 = df.iloc[col0_count, 32] if col0_count < df_rows else None
        if not df.iloc[5:, 44].isnull().all():
            table_catch3 = df.iloc[col0_count, 44] if col0_count < df_rows else None
    else:
        # 初始化sql关联字段，匹配对应系统标识 table_L
        if not df.iloc[5:, 14].isnull().all():
            # 去除第16列的空值
            # df_no_na = df.iloc[:, 16].dropna()
            # 获取最后一个值,作为表关联，赋值table+table_falg
            # lastname = df_no_na.iloc[-1]
            table_catch1 = common.get_table_catch_sys(common.FLAG_SYS_1, df.iloc[col0_count,16] if col0_count < df_rows else None)
        if not df.iloc[5:, 26].isnull().all():
            table_catch2 = common.get_table_catch_sys(common.FLAG_SYS_2, df.iloc[col0_count,28] if col0_count < df_rows else None)
        if not df.iloc[5:, 38].isnull().all():
            table_catch3 = common.get_table_catch_sys(common.FLAG_SYS_3, df.iloc[col0_count,40] if col0_count < df_rows else None)

    # 初始化表英文名，因为源系统中英文位置会互换。。。
    if re.match(r'[a-zA-Z]', df.columns[1][0]):
        tab_en_cn = str(df.columns[1])
    else:
        tab_en_cn = str(df.iloc[0, 1])

    # 初始化：目标表 实体类集合
    for index, row in df.iterrows():
        if index <= 2: continue
        mainList.append(
            Bean.MainBean(tab_en_cn, df.iloc[index, 0], df.iloc[index, 1], df.iloc[index, 2], df.iloc[index, 3],
                          df.iloc[index, 4], df.iloc[index, 5], df.iloc[index, 6], df.iloc[index, 7], df.iloc[index, 8],
                          df.iloc[index, 9], df.iloc[index, 10], df.iloc[index, 11], df.iloc[index, 12]))
        # 根据df.iloc[index, 4]判断是否为主键，若 df.iloc[index, 4] = '是' ,则df.iloc[index, 1]存入primaryKeyList
        if df.iloc[index, 4] in (common.PRIMARY_KEY,'Y'):
            primaryKeyList.append(index)
        # 初始化mapBean,根据'原表字段英文名'列判断，都为空则该系统映射，否则有字段映射
        # 用pandas判断16列第5行以后的值是否为都空，第一段系统
        if not df.iloc[5:, 14].isnull().all():
            # 初始化Bean.MapBean,并存入mapList1。mapbean初始化的参数从13开始到24，df.iloc[index,13]
            mapList_1.append(
                Bean.MapBean(df.iloc[index, 13], df.iloc[index, 14], df.iloc[index, 15], df.iloc[index, 20] if MAPPING_KEY else df.iloc[index, 16],
                             df.iloc[index, 17], df.iloc[index, 18], df.iloc[index, 19], df.iloc[index, 20],
                             df.iloc[index, 21], df.iloc[index, 22], df.iloc[index, 23], df.iloc[index, 24],
                             df.iloc[index, 4], common.FLAG_SYS_1, table_catch1))
        if not df.iloc[5:, 26].isnull().all():
            # 初始化Bean.MapBean,并存入mapList2。mapbean初始化的参数从25开始到36，df.iloc[index,25]
            mapList_2.append(
                Bean.MapBean(df.iloc[index, 25], df.iloc[index, 26], df.iloc[index, 27], df.iloc[index, 32]if MAPPING_KEY else df.iloc[index, 28],
                             df.iloc[index, 29], df.iloc[index, 30], df.iloc[index, 31], df.iloc[index, 32],
                             df.iloc[index, 33], df.iloc[index, 34], df.iloc[index, 35], df.iloc[index, 36],
                             df.iloc[index, 4], common.FLAG_SYS_2, table_catch2))
        if not df.iloc[5:, 38].isnull().all():
            # 初始化Bean.MapBean,并存入mapList3。mapbean初始化的参数从37开始到48，df.iloc[index,37]
            mapList_3.append(
                Bean.MapBean(df.iloc[index, 37], df.iloc[index, 38], df.iloc[index, 39], df.iloc[index, 44]if MAPPING_KEY else df.iloc[index, 40],
                             df.iloc[index, 41], df.iloc[index, 42], df.iloc[index, 43], df.iloc[index, 44],
                             df.iloc[index, 45], df.iloc[index, 46], df.iloc[index, 47], df.iloc[index, 48],
                             df.iloc[index, 4], common.FLAG_SYS_3, table_catch3))

    # 生成新列名‘字段取值的正确性’
    df['字段取值的正确性'] = None
    # 生成新列名‘正确性验证sql’
    df['正确性验证sql'] = None
    df['备注'] = None
    # 获取这两列的索引 '字段取值的正确性','正确性验证sql'
    col_num_ver_field = df.columns.get_loc('字段取值的正确性')
    col_num_ver_sql = df.columns.get_loc('正确性验证sql')
    col_num_remark = df.columns.get_loc('备注')
    # 对len1 赋值，当 len(mapList_1) > 0 赋值1，否则赋值0
    len1 = 1 if len(mapList_1) > 0 else 0
    len2 = 1 if len(mapList_2) > 0 else 0
    len3 = 1 if len(mapList_3) > 0 else 0

    # '字段取值的正确性','正确性验证sql'
    for index, row in df.iterrows():
        if index < 3:
            continue
        row_remark = ""  # 行备注
        sql1 = f"select count(1) as tcount from {mainList[index - 3].table_name} t, ( "
        if len1 > 0:
            templist = mapList_1
            # 遍历primarykeyList,拼接sql
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                else:
                    sql1 += '\nselect '
                sql1 += f"{templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            if templist[index - 3].is_primary_key not in ("是", 'Y'):
                sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                         f"{templist[index - 3].table_name} \n")
            else:
                sql1 += (f"{templist[index - 3].table_name} \n")
            if templist[index - 3].source_field_en == "Temp" + templist[index - 3].table_flag:
                row_remark += f"{df.iloc[0, 13]}:无[{mainList[index - 3].field_en}]字段映射关系\n"
        if len2 > 0:
            templist = mapList_2
            if len1 > 0:
                sql1 += f"union all \n "
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                else:
                    sql1 += 'select '
                sql1 += f"{templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            if templist[index - 3].is_primary_key not in ("是", 'Y'):
                sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                         f"{templist[index - 3].table_name} \n")
            else:
                sql1 += (f"{templist[index - 3].table_name} \n")
            if templist[index - 3].source_field_en == "Temp" + templist[index - 3].table_flag:
                row_remark += f"{df.iloc[0, 25]}:无[{mainList[index - 3].field_en}]字段映射关系\n"

        if len3 > 0:
            templist = mapList_3
            if len2 > 0 or len1 > 0:
                sql1 += f"union all \n "
            for i in range(len(primaryKeyList)):  # 系统1 主键拼接
                if i > 0:
                    sql1 += ','
                else:
                    sql1 += 'select '
                sql1 += f"{templist[primaryKeyList[i] - 3].source_field_en} as {mainList[primaryKeyList[i] - 3].field_en}\n"
            if templist[index - 3].is_primary_key not in ("是", 'Y'):
                sql1 += (f",{templist[index - 3].source_field_en} as {mainList[index - 3].field_en} \n"
                         f"{templist[index - 3].table_name} \n")
            else:
                sql1 += (f"{templist[index - 3].table_name} \n")
            if templist[index - 3].source_field_en == "Temp" + templist[index - 3].table_flag:
                row_remark += f"{df.iloc[0, 37]}:无[{mainList[index - 3].field_en}]字段映射关系"

        sql1 += ") t1 \n where "
        # sql 拼接主键的关联
        for i in range(len(primaryKeyList)):
            if i > 0:
                sql1 += 'and '
            sql1 += f"t.{mainList[primaryKeyList[i] - 3].field_en} = t1.{mainList[primaryKeyList[i] - 3].field_en} \n"
        if mainList[index - 3].is_primary_key != common.PRIMARY_KEY:
            sql1 += f"and nvl(t.{mainList[index - 3].field_en},'') = nvl(t1.{mainList[index - 3].field_en},'') \n"

        if mainList[index - 3].field_en != '':
            df.loc[index, df.columns[
                col_num_ver_field]] = f"验证：{mainList[index - 3].field_cn}({mainList[index - 3].field_en})取值的正确性"
            df.loc[index, df.columns[col_num_ver_sql]] = sql1
        df.loc[index, df.columns[col_num_remark]] = row_remark
    # 生成新列名‘字段取值的正确性’
    df['验证码值'] = None
    # 生成新列名‘正确性验证sql’
    df['验证码值sql'] = None
    # 获取这两列的索引 '字段取值的正确性','正确性验证sql'
    col_num_code_field = df.columns.get_loc('验证码值')
    col_num_code_sql = df.columns.get_loc('验证码值sql')
    # 验证码值
    for index, row in df.iterrows():
        if index < 3:
            continue
        if (mainList[index - 3].value_constraint is not None) and len(mainList[index - 3].value_constraint) > 0:
            df.loc[index, df.columns[
                col_num_code_field]] = f"验证：{mainList[index - 3].field_cn}({mainList[index - 3].field_en})码值在落标码值范围内"
            # result = [i.split('-')[0] for i in mainList[index - 3].value_constraint.split()]
            result = [x.split('-')[0] for x in mainList[index - 3].value_constraint.split('\n')]
            result = str(result).replace('[', "(")
            result = str(result).replace(']', ")")
            sql1 = f"select count(1) as tcount from {mainList[index - 3].table_name} where {mainList[index - 3].field_en} not in {result}"
            df.loc[index, df.columns[col_num_code_sql]] = sql1

    # 生成新列名‘字段取值的正确性’‘正确性验证sql’
    df['混合列'] = None
    df['混合sql'] = None
    df['compareTo'] = None
    # 获取这两列的索引 '字段取值的正确性','正确性验证sql'
    col_num_hh_field = df.columns.get_loc('混合列')
    col_num_hh_sql = df.columns.get_loc('混合sql')
    col_num_ct_sql = df.columns.get_loc('compareTo')
    # 遍历primarykeyList,拼接sql
    sql5 = f"select COUNT(DISTINCT "
    sql6 = f"select COUNT(1) as tcount from {mainList[0].table_name} where "
    # nvl(mid_third_iou_id,'')='' or  nvl(tenant_id,'')=''
    for i in range(len(primaryKeyList)):  # 系统1 主键拼接
        if i > 0:
            sql5 += ','
            sql6 += ' or '
        sql5 += f"{mainList[primaryKeyList[i] - 3].field_en}"
        sql6 += f"nvl({mainList[primaryKeyList[i] - 3].field_en},'') = ''"
    sql5 += f") as tcount from {mainList[index - 3].table_name}"

    df.loc[3, df.columns[col_num_hh_field]] = "验证：迁出表与中间表迁移数据总数的一致性"
    df.loc[3, df.columns[col_num_hh_sql]] = f"select count(1) as tcount from {mainList[0].table_name}"

    # 遍历mainList
    sql4 = "select \nsum("
    sql4_cnt = 0
    sql7 = "select \nsum("
    sqlcp7 = "select \n0 "
    sql7_cnt = 0
    for i, mb in enumerate(mainList):
        # sum(金额)
        if 'DECIMAL' in mb.data_type.upper():
            if sql4_cnt > 0:
                sql4 += ',sum('
            sql4 += f"nvl({mb.field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
            sql4_cnt += 1
        if mb.is_null in ('否', 'N'):
            if sql7_cnt > 0:
                sql7 += ',sum('
                sqlcp7 += ',0'
                # ,sum(case when nvl(left_repay_principal,'') = '' then 1 else 0 end) as left_repay_principal
            sql7 += f"case when nvl({mb.field_en},'')='' then 1 else 0 end ) as {mb.field_en}  /* {mb.field_cn} */\n"
            sqlcp7 += f" as {mb.field_en}  /* {mb.field_cn} */\n"
            sql7_cnt += 1
        if i == len(mainList) - 1:
            sql7 += f"from {mainList[0].table_name}"
            sqlcp7 += f"from dual"
    # 如果有金额字段，则输出sql
    if sql4_cnt > 0:
        df.loc[4, df.columns[col_num_hh_field]] = "验证：迁出表与中间表金额相关字段汇总的一致性"
        df.loc[4, df.columns[col_num_hh_sql]] = sql4 + f"from {mainList[0].table_name}"
    df.loc[5, df.columns[col_num_hh_field]] = "验证：目标表数据的唯一性"
    df.loc[5, df.columns[col_num_hh_sql]] = sql5
    df.loc[6, df.columns[col_num_hh_field]] = "验证：主键不为空"
    df.loc[6, df.columns[col_num_hh_sql]] = sql6
    df.loc[7, df.columns[col_num_hh_field]] = "验证：必输字段不为空"
    df.loc[7, df.columns[col_num_hh_sql]] = sql7

    # compare to 数据总量
    sqlcp3 = f"select sum(tcount) as tcount from ("
    if len1 > 0:
        sqlcp3 += f"\nselect count(1) as tcount {mapList_1[0].table_name} "
    if len2 > 0:
        if len1 > 0:
            sqlcp3 += f"\nunion all"
        sqlcp3 += f"\nselect count(1) as tcount {mapList_2[0].table_name} "
    if len3 > 0:
        if len1 > 0 or len2 > 0:
            sqlcp3 += f"\nunion all"
        sqlcp3 += f"\nselect count(1) as tcount {mapList_3[0].table_name} "
    sqlcp3 += f"\n) t"
    df.loc[3, df.columns[col_num_ct_sql]] = sqlcp3

    # compare to 金额
    sqlcp4 = ""
    sqlcp4_cnt = 0
    sqlcp4_1 = ""
    sqlcp4_2 = ""
    sqlcp4_3 = ""
    for i, mb in enumerate(mainList):
        # sum(金额)
        if 'DECIMAL' in mb.data_type.upper():
            if sqlcp4_cnt == 0:
                sqlcp4 = f"select sum("
                sqlcp4 += f"{mb.field_en}) as {mb.field_en}  /* {mb.field_cn} */\n"
            else:
                sqlcp4 += ',sum('
                sqlcp4 += f"{mb.field_en}) as {mb.field_en}  /* {mb.field_cn} */\n"

            if len1 > 0:
                if sqlcp4_cnt == 0:
                    sqlcp4_1 += f"select \nsum("
                    sqlcp4_1 += f"nvl({mapList_1[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
                else:
                    sqlcp4_1 += f",sum("
                    sqlcp4_1 += f"nvl({mapList_1[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
            if len2 > 0:
                if sqlcp4_cnt == 0 :
                    if len1 > 0:
                        sqlcp4_2 += f"union all\n"
                    sqlcp4_2 += f"select \nsum("
                    sqlcp4_2 += f"nvl({mapList_2[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
                else:
                    sqlcp4_2 += f",sum("
                    sqlcp4_2 += f"nvl({mapList_2[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
            if len3 > 0:
                if sqlcp4_cnt == 0 :
                    if len1 > 0 or len2 > 0:
                        sqlcp4_3 += f"union all\n"
                    sqlcp4_3 += f"select \nsum("
                    sqlcp4_3 += f"nvl({mapList_3[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
                else:
                    sqlcp4_3 += f",sum("
                    sqlcp4_3 += f"nvl({mapList_3[i].source_field_en},0)) as {mb.field_en}  /* {mb.field_cn} */\n"
            sqlcp4_cnt += 1
        if i == len(mainList) - 1:
            if len1 + len2 + len3 >= 1:
                sqlcp4 += "from (\n"
                if len1 > 0:
                    sqlcp4_1 += f"{mapList_1[0].table_name}\n"
                if len2 > 0:
                    sqlcp4_2 += f"{mapList_2[0].table_name}\n"
                if len3 > 0:
                    sqlcp4_3 += f"{mapList_3[0].table_name}\n"
            sqlcp4 += sqlcp4_1 + sqlcp4_2 + sqlcp4_3
            if len1 + len2 + len3 >= 1:
                sqlcp4 += ") t\n"
            if sqlcp4_cnt > 0:
                df.loc[4, df.columns[col_num_ct_sql]] = sqlcp4
            df.loc[5, df.columns[col_num_ct_sql]] = f"select count(1) as tcount from {mainList[0].table_name}"
            df.loc[6, df.columns[col_num_ct_sql]] = f"select 0 as tcount from dual"
            df.loc[7, df.columns[col_num_ct_sql]] = sqlcp7

    df_all[sheet] = df
    df_all2[sheet] = common.fz(df, ndf)
# 删除之前是生成的文件，并重新生成文件
common.del_file()
# 将所有的sheet页合并成一个文件但每个sheet页写入到文件的不同工作表中
with pd.ExcelWriter(common.FILE_URL_OUT, engine='xlsxwriter') as writer:
    for sheet_name, df_sheet in df_all.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
print("生成文件成功：" + common.FILE_URL_OUT)

with pd.ExcelWriter(common.FILE_URL_OUT2, engine='xlsxwriter') as writer:
    for sheet_name, df_sheet in df_all2.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
print("生成文件成功：" + common.FILE_URL_OUT2)
