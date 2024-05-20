import os
import re
import sys

PRIMARY_KEY = "是"
# exlce中迁出的系统标识
FLAG_SYS_1 = "L"
FLAG_SYS_2 = "P"
FLAG_SYS_3 = "S"
# 作者
AUTHOR = "脚本"
# 时间
CREATE_TIME = "20210510"

test_file_clos = ['案例名称', '案例描述', '案例标签', '数据源1', '执行SQL1', '数据源2', '执行SQL2', '验证方式',
                  'SQL返回字段名', '结果对比方式', '预期结果（单库比较时填写）', '问题级别', '设计人', '创建时间',
                  '案例有效性', '备注']
# test_file_des = [
#     "描述此条案例对应的具体测试意图\n注：①同一个表中，测试意图不能重复 ②语句通顺、可读、清晰明了，便于读者有效获取测试验证的意图",
#     "描述具体验证表\n格式：表英文名称_表中文名称",
#     "对案例进行归类，\n包含但不限于：汇总检查，明细检查，字段约束检查，数据落标检查",
#     "待验证数据库，需要与测试工具配置一致，对应加工前数据", "数据来源1中取数SQL脚本",
#     "待验证数据库，需要与测试工具中参数配置-数据源配置中一致，对应加工后数据存放的数据库",
#     "据来源2中取数SQL脚本", "固定值：结果集", "固定值：空", "固定值：等于", "固定值：空", "固定值：严重",
#     "案例编写人名称\n注：若该条案例存在修订，则更新为最新修订人", "描述案例新增的时间，YYYY/MM/DD",
#     "此条案例操作类型及有效性说明，值类型（有效【默认】，无效）\n注：首次导入到测试管理平台中，均为有效，因此默认值-有效。",
#     "此条案例的备注说明"]
FILE_NAME_L="date_bk_l.xlsx"
FILE_NAME_P="date_bk_p.xlsx"
FILE_NAME_S="date_bk_s.xlsx"
# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 设置输出文件名，如果存在先就删除，文件打开状态无法删除
file_to_delete = "date_bk.xlsx"
file_to_delete2 = "date_tar_bk.xlsx"
# FILE_URL_IN = os.path.join(same_level_directory, "xintou_dev.xlsx")
FILE_URL_IN = os.path.join(same_level_directory, "pls_迁出至新信投_mapping_0510_base.xlsx")
FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
FILE_URL_OUT2 = os.path.join(same_level_directory, file_to_delete2)
FILE_URL_OUT_L = os.path.join(same_level_directory, FILE_NAME_L)
FILE_URL_OUT_P = os.path.join(same_level_directory, FILE_NAME_P)
FILE_URL_OUT_S = os.path.join(same_level_directory, FILE_NAME_S)


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
        print("文件：", file_to_delete, " 要在关闭状态才能删除重建哦！！")
        # 如果文件存在，则删除它
        os.remove(FILE_URL_OUT)
        print(f"文件 {FILE_URL_OUT} 已删除。")
    else:
        print(f"文件 {FILE_URL_OUT} 不存在。")
    if os.path.exists(FILE_URL_OUT_L):
        # 如果文件存在，则删除它
        os.remove(FILE_URL_OUT_L)
    if os.path.exists(FILE_URL_OUT_P):
        # 如果文件存在，则删除它
        os.remove(FILE_URL_OUT_P)
    if os.path.exists(FILE_URL_OUT_S):
        # 如果文件存在，则删除它
        os.remove(FILE_URL_OUT_S)


def init_pd_config(pd):
    # 设置显示完整的列
    pd.set_option('display.max_columns', None)
    # 设置显示完整的行
    pd.set_option('display.max_rows', None)
    pd.options.mode.copy_on_write = True
    return pd





# source_df,tar_df,返回tar_df
def fz(sdf, tdf,sys_flag):
    # 循环从0开始，循环5次
    col_num_hh_field = sdf.columns.get_loc('混合列')
    col_num_hh_sql = sdf.columns.get_loc('混合sql')
    col_num_ct_sql = sdf.columns.get_loc('compareTo')
    col_num_ver_field = sdf.columns.get_loc('字段取值的正确性')
    col_num_ver_sql = sdf.columns.get_loc('正确性验证sql')
    col_num_remark = sdf.columns.get_loc('备注')
    col_num_code_field = sdf.columns.get_loc('验证码值')
    col_num_code_sql = sdf.columns.get_loc('验证码值sql')
    # 获取pandas列名集合
    init_row_nm=2
    sum_num = sdf[sdf.columns[col_num_hh_field]].notnull().sum()

    if re.match(r'[a-zA-Z]', sdf.columns[1][0]):
        tab_en=str(sdf.columns[1])
        tab_en_cn =  str(sdf.columns[1]) + "-" + str(sdf.iloc[0, 1])
    else:
        tab_en = str(sdf.iloc[0, 1])
        tab_en_cn = str(sdf.iloc[0, 1])+ "-" +str(sdf.columns[1])
    for i in range(5):
        # sdf.loc[i + 3, sdf.columns[col_num_code_sql]]
        for index, column in enumerate(tdf.columns):
            if i==1 and (sdf.loc[i + 3, sdf.columns[col_num_hh_field]] is None or sdf.loc[i + 3, sdf.columns[col_num_hh_field]] == ""):
                continue
            elif index == 0:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_hh_field]]
            elif index == 1:
                tdf.loc[i + init_row_nm, column] = tab_en_cn
            elif index == 2:
                #字段约束检查
                if "必输字段不为空" in sdf.loc[i + 3, sdf.columns[col_num_hh_field]]:
                    tdf.loc[i + init_row_nm, column] = "字段约束检查"
                else:
                    tdf.loc[i + init_row_nm, column] = "汇总检查"
            elif index == 3:
                tdf.loc[i + init_row_nm, column] = sys_flag+"数据库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_hh_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag+"数据库"
            elif index == 6:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_ct_sql]]
            elif index == 7:
                tdf.loc[i + init_row_nm, column] = "结果集"
            elif index == 8:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 9:
                tdf.loc[i + init_row_nm, column] = "等于"
            elif index == 10:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 11:
                tdf.loc[i + init_row_nm, column] = "严重"
            elif index == 12:
                tdf.loc[i + init_row_nm, column] = AUTHOR
            elif index == 13:
                tdf.loc[i + init_row_nm, column] = CREATE_TIME
            elif index == 14:
                tdf.loc[i + init_row_nm, column] = "有效"
            elif index == 15:
                tdf.loc[i + init_row_nm, column] = ""
        # df第一列有值的行数
        init_row_nm+=5
        desc_nm = sdf[sdf.columns[col_num_ver_field]].notnull().sum()
    for i in range(desc_nm):
        for index, column in enumerate(tdf.columns):
            if index == 0:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_ver_field]]
            elif index == 1:
                tdf.loc[i + init_row_nm, column] = tab_en_cn
            elif index == 2:
                tdf.loc[i + init_row_nm, column] = "明细检查"
            elif index == 3:
                tdf.loc[i + init_row_nm, column] = sys_flag+"数据库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_ver_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag+"数据库"
            elif index == 6:
                tdf.loc[i + init_row_nm, column] = f"select count(1) as tcount from {tab_en}"
            elif index == 7:
                tdf.loc[i + init_row_nm, column] = "结果集"
            elif index == 8:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 9:
                tdf.loc[i + init_row_nm, column] = "等于"
            elif index == 10:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 11:
                tdf.loc[i + init_row_nm, column] = "严重"
            elif index == 12:
                tdf.loc[i + init_row_nm, column] = AUTHOR
            elif index == 13:
                tdf.loc[i + init_row_nm, column] = CREATE_TIME
            elif index == 14:
                tdf.loc[i + init_row_nm, column] = "有效"
            elif index == 15:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_remark]]
    init_row_nm+=desc_nm
    ver_nm=sdf[sdf.columns[col_num_code_field]].notnull().sum()
    for i in range(desc_nm):
        for index, column in enumerate(tdf.columns):
            if i==1 and (sdf.loc[i + 2, sdf.columns[col_num_code_field]] is None or sdf.loc[i + 2, sdf.columns[col_num_code_field]] == ""):
                continue
            elif index == 0:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_code_field]]
            elif index == 1:
                tdf.loc[i + init_row_nm, column] = tab_en_cn
            elif index == 2:
                tdf.loc[i + init_row_nm, column] = "数据落标检查"
            elif index == 3:
                tdf.loc[i + init_row_nm, column] = sys_flag + "数据库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_code_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag + "数据库"
            elif index == 6:
                tdf.loc[i + init_row_nm, column] = "select 0 as tcount from dual"
            elif index == 7:
                tdf.loc[i + init_row_nm, column] = "结果集"
            elif index == 8:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 9:
                tdf.loc[i + init_row_nm, column] = "等于"
            elif index == 10:
                tdf.loc[i + init_row_nm, column] = ""
            elif index == 11:
                tdf.loc[i + init_row_nm, column] = "严重"
            elif index == 12:
                tdf.loc[i + init_row_nm, column] = AUTHOR
            elif index == 13:
                tdf.loc[i + init_row_nm, column] = CREATE_TIME
            elif index == 14:
                tdf.loc[i + init_row_nm, column] = "有效"
            elif index == 15:
                tdf.loc[i + init_row_nm, column] = ""
    ##下面4行用于删除包含用于填充空mapping的临时字段 Temp 的行
    tdf = tdf.dropna(axis=0, how='any')
    tdf = tdf[~tdf['执行SQL1'].str.contains('Temp')]
    tdf = tdf[~tdf['执行SQL2'].str.contains('Temp')]
    #删除空行
    tdf = tdf.dropna(axis=0, how='any')
    return tdf
