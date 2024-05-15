# 创建实体类，属性名和属性类型如下：
# 源系统	源表英文名	源表中文名	源表字段英名	源表字段中文名	数据类型	码值说明	映射规则	SQL	业务牵头部门	业务对接人	备注, 12个属性,用python创建实体类,名称尽量简洁
import re


class MapBean:
    def __init__(self, source_system, source_table_en, source_table_cn, source_field_en, source_field_cn, data_type,
                 code_value, mapping_rule, sql, business_department, business_contact, remark, is_primary_key,
                 table_flag, table_name: str):
        self.source_system = str(source_system).replace('nan', '')
        self.source_table_en = str(source_table_en).replace('nan', '')
        self.source_table_cn = str(source_table_cn).replace('nan', '')
        self.source_field_en = str(source_field_en).replace('nan', '')
        self.source_field_cn = str(source_field_cn).replace('nan', '')
        self.data_type = str(data_type).replace('nan', '')
        self.code_value = str(code_value).replace('nan', '')
        self.mapping_rule = str(mapping_rule).replace('nan', '')
        self.sql = str(sql)
        self.business_department = str(business_department).replace('nan', '')
        self.business_contact = str(business_contact).replace('nan', '')
        self.remark = str(remark).replace('nan', '')
        self.is_primary_key = str(is_primary_key).replace('nan', '')
        self.table_flag = str(table_flag).replace('nan', '')
        self.table_name = ""  # 表关联条件
        # 如果source_field_en包含'('，就将'.'和括号之间的内容去掉，如果不包含'('，就保留'.'之后的内容，如果没有'.'，就保留原内容
        if '.' in self.source_field_en:
            if '(' in self.source_field_en:
                # 截取source_field_en 开始到'('之间的内容
                self.field_no_dot = source_field_en.replace(
                    source_field_en[source_field_en.find('(') + 1:source_field_en.find('.') + 1], '')
            else:
                self.field_no_dot = source_field_en[source_field_en.find('.') + 1:]
        else:
            self.field_no_dot = source_field_en
        #  给空字段赋值 Temp+table_flag
        if self.source_field_en == '':
            self.source_field_en = 'Temp' + table_flag
        #  给表关联条件赋值，如果为空，就赋值为 table+table_flag
        if table_name is not None and table_name != 'NAN' and re.match(r'[a-zA-Z]', table_name.strip()):
            if 'from' not in table_name.strip().lower()[0:5]:
                self.table_name = 'from ' + table_name
            else:
                self.table_name = table_name
        else:
            self.table_name = 'from table' + table_flag

    def __str__(self):
        return self.source_system + "," + self.source_table_en + "," + self.source_table_cn + "," + self.source_field_en + "," + self.source_field_cn + "," + self.data_type + "," + self.code_value + "," + self.mapping_rule + "," + self.sql + "," + self.business_department + "," + self.business_contact + "," + self.remark

    def __repr__(self):
        return self.source_system + "," + self.source_table_en + "," + self.source_table_cn + "," + self.source_field_en + "," + self.source_field_cn + "," + self.data_type + "," + self.code_value + "," + self.mapping_rule + "," + self.sql + "," + self.business_department + "," + self.business_contact + "," + self.remark


# 创建实体类对象,类型MainBean,字段名称如下：

# 字段序号	字段英文名	字段中文名	数据类型	是否主键	是否空值	业务说明	值域类型	值域约束	业务牵头部门	业务对接人	最后更新时间	备注，名称尽量简洁
class MainBean:
    def __init__(self, table_name, field_index, field_en, field_cn, data_type, is_primary_key, is_null,
                 business_explain, value_type, value_constraint, business_department, business_contact,
                 last_update_time, remark):
        self.table_name = str(table_name).replace('nan', '')
        self.field_index = str(field_index).replace('nan', '')
        self.field_en = str(field_en).replace('nan', '')
        self.field_cn = str(field_cn).replace('nan', '')
        self.data_type = str(data_type).replace('nan', '')
        self.is_primary_key = str(is_primary_key).replace('nan', '')
        self.is_null = str(is_null).replace('nan', '')
        self.business_explain = str(business_explain).replace('nan', '')
        self.value_type = str(value_type).replace('nan', '')
        self.value_constraint = str(value_constraint).replace('nan', '')
        self.business_department = str(business_department).replace('nan', '')
        self.business_contact = str(business_contact).replace('nan', '')
        self.last_update_time = str(last_update_time).replace('nan', '')
        self.remark = str(remark).replace('nan', '')
        if (self.is_primary_key == '是') and (self.field_en == ''):
            self.field_en = 'Temp'

    def __str__(self):
        return self.field_index + "," + self.field_en + "," + self.field_cn + "," + self.data_type + "," + self.is_primary_key + "," + self.is_null + "," + self.business_explain + "," + self.value_type + "," + self.value_constraint + "," + self.business_department + "," + self.business_contact + "," + self.last_update_time + "," + self.remark

    def __repr__(self):
        return self.field_index + "," + self.field_en + "," + self.field_cn + "," + self.data_type + "," + self.is_primary_key + "," + self.is_null + "," + self.business_explain + "," + self.value_type + "," + self.value_constraint + "," + self.business_department + "," + self.business_contact + "," + self.last_update_time + "," + self.remark
