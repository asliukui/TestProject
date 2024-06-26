import os
import re
import sys

import pandas as pd

PRIMARY_KEY = "是"
# exlce中迁出的系统标识
FLAG_SYS_L = "L"
FLAG_SYS_P = "P"
FLAG_SYS_S = "S"
L_SCHEMA = "LSBKSC."
S_SCHEMA = "XINDAI0331."
P_SCHEMA = ""
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
FILE_NAME_L = "date_bk_l.xlsx"
FILE_NAME_P = "date_bk_p.xlsx"
FILE_NAME_S = "date_bk_s.xlsx"

# 获取当前脚本的路径
script_path = os.path.abspath(__file__)
# 获取同级目录
same_level_directory = os.path.dirname(script_path)
# 设置输出文件名，如果存在先就删除，文件打开状态无法删除
file_to_delete = "date_bk.xlsx"
file_to_delete2 = "date_tar_bk.xlsx"
# FILE_URL_IN = os.path.join(same_level_directory, "xintou_dev.xlsx")
# FILE_URL_IN = os.path.join(same_level_directory, "SCB_新一代新信投项目群_新信投系统中间表数据据映射mapping-V0.05.xlsx")
FILE_URL_IN = os.path.join(same_level_directory, "SCB_新一代新信投项目群_新信投系统中间表数据据映射mapping-V0.081-汇总版.xlsx")
FILE_URL_OUT = os.path.join(same_level_directory, file_to_delete)
FILE_URL_OUT2 = os.path.join(same_level_directory, file_to_delete2)

FILE_NAME_MERGE_L = "date_bk_merge_l.xlsx"
FILE_NAME_MERGE_P = "date_bk_merge_p.xlsx"
FILE_NAME_MERGE_S = "date_bk_merge_s.xlsx"
FILE_URL_OUT_L = os.path.join(same_level_directory, FILE_NAME_L)
FILE_URL_OUT_P = os.path.join(same_level_directory, FILE_NAME_P)
FILE_URL_OUT_S = os.path.join(same_level_directory, FILE_NAME_S)
FILE_URL_OUT_MERGE_L = os.path.join(same_level_directory, FILE_NAME_MERGE_L)
FILE_URL_OUT_MERGE_P = os.path.join(same_level_directory, FILE_NAME_MERGE_P)
FILE_URL_OUT_MERGE_S = os.path.join(same_level_directory, FILE_NAME_MERGE_S)

# 字段类型
field_num_types = ['DECIMAL', 'INT']
# 是否必输，源系统可能反，要随时根据上游版本改动
field_not_null_flag = ['否', 'N']
field_is_null_flag = ['是', 'Y']
# 系统表名
table_m = []
table_s = ['ENT_BONDISSUE', 'ENT_IPO', 'AA', 'ACCOUNTING_CATALOG', 'ACCOUNTING_LIBRARY',
           'ACCT_BUSINESS_SUBJECT_MAPPING', 'ACCT_BUSINESS_SUBJECT_RULE', 'ACCT_CORE_ACCOUNT', 'ACCT_FILE_NAME',
           'ACCT_LOAN', 'ACCT_LOAN_QUERY', 'ACCT_TRANSACTION', 'ALS_DESIGN', 'ALS_TABLE', 'ALS_TABLE_METADATA',
           'ALS_TABLE_PERFORMANCE', 'ALS_TABLE_RELATIVE', 'APPLY_RELATIVE', 'APPROVE_DATA', 'APPROVE_DATA_TEMP',
           'AREA_LIBRARY', 'ASYNC_TASK_RECORD', 'AUDIT_INFO', 'AWE_DICT_ERRMSG', 'AWE_DO_CATALOG',
           'AWE_DO_COL_VALIDATE', 'AWE_DO_EVENT', 'AWE_DO_GROUP', 'AWE_DO_LIBRARY', 'AWE_DO_MODES', 'AWE_DO_VALIDATE',
           'AWE_DO_VALIDATE_CATALOG', 'AWE_DW_CONTEXT', 'AWE_ERPT_CATALOG', 'AWE_ERPT_DATA', 'AWE_ERPT_DEF',
           'AWE_ERPT_MAP', 'AWE_ERPT_OFFLINE', 'AWE_ERPT_RECORD', 'AWE_ERPT_TYPE', 'AWE_FUNCTION_INFO',
           'AWE_GROUP_CATALOG', 'AWE_GROUP_CLASSIFY', 'AWE_GROUP_ITEM', 'AWE_HREF_INFO', 'AWE_JSP_RUNTIME',
           'AWE_MENU_INFO', 'AWE_QUICK_HREF', 'AWE_ROLE_FUNCTION', 'AWE_ROLE_INFO', 'AWE_ROLE_MENU', 'AWE_TASK_INFO',
           'BATCH_NOTE_MESSAGE', 'BATCH_TASKSTATUS', 'BATCHSN', 'BUSINESS_APPLY', 'BUSINESS_APPROVE',
           'BUSINESS_CONTRACT', 'BUSINESS_CONTRACT_BF', 'BUSINESS_CONTRACT_BF_L', 'BUSINESS_CONTRACT_BF_P',
           'BUSINESS_DUEBILL', 'BUSINESS_DUEBILL_BWTJ', 'BUSINESS_DUEBILL_DKTJ', 'BUSINESS_FREEZE_LOG',
           'BUSINESS_PUTOUT', 'BUSINESS_PUTOUT_BF_L', 'BUSINESS_PUTOUT_BF_P', 'BUSINESS_PUTOUT_ONLYONE',
           'BUSINESS_RELATIVE', 'BUSINESS_SORT', 'BUSINESS_TYPE', 'BUSINESS_USE_INFO', 'BUSINESS_USE_INFO_CX',
           'BUSINESSARG_FUNCTIONNO', 'BUSINESSTYPE_ARG', 'BUSINESSTYPE_LIMIT', 'CL_DIVIDE', 'CL_ERROR_TYPE',
           'CL_LIMITATION_TYPE', 'CL_OCCUPY', 'CL_TEAM', 'CL_TYPE', 'CL_USERULE', 'CLASS_CATALOG', 'CLASS_METHOD',
           'CLASSIFY_CATALOG', 'CLASSIFY_MODEL', 'CLASSIFY_RECORD', 'CMS_COL_PARAM', 'CMS_COLLATERALDONO_INFO',
           'CMS_COLLATERALTYPE_INFO', 'CMS_COLPOLICY_INFO', 'CMS_COLTYPE_EVAMOD', 'CMS_COLTYPE_ORG', 'CNAPSBANKINFO',
           'CODE_CATALOG', 'CODE_INFO', 'CODE_LIBRARY', 'CODE_TEMP', 'CONCEDE_INFO', 'CONDITION_RULE',
           'CONTRACT_RELATIVE', 'COST_INFO', 'CREDIT_CODE_BAK', 'CREDITINQUIRY_ORG', 'CREDITINQUIRY_USER',
           'CRQ_ACCOUNT', 'CRQ_PARA', 'CUSTOMER_ADDRESS', 'CUSTOMER_BELONG', 'CUSTOMER_CERT', 'CUSTOMER_FSRECORD',
           'CUSTOMER_IMPORT_LOG', 'CUSTOMER_INFO', 'CUSTOMER_INFO_CHANGE', 'CUSTOMER_MERGE', 'CUSTOMER_MODEL',
           'CUSTOMER_RELATIVE', 'CUSTOMER_SPECIAL', 'CUSTOMER_TEL', 'CUSTOMER_TEMP_DOUBLE', 'CUSTOMER_TRANSFER',
           'DATAOBJECT_CATALOG', 'DATAOBJECT_COL_VALID', 'DATAOBJECT_GROUP', 'DATAOBJECT_LIBRARY', 'DBEXTENSION',
           'DCZY_TRADE_CONSTANS', 'DEPOSIT_TEMP', 'DOC_ATTACHMENT', 'DOC_ATTACHMENT_TASK', 'DOC_LIBRARY',
           'DOC_RELATIVE', 'DOCUMENT_CATALOG', 'DOCUMENT_DATA', 'DOCUMENT_DATA_BAK', 'DOCUMENT_LIBRARY',
           'DOCUMENT_RECORD', 'DS_SIGHT', 'DS_SIGHT_SET', 'DWTEMPLATE_INFO', 'ECM_IMAGE_TYPE', 'ECM_PRDIMAGE_RELA',
           'ENT_AUTH', 'ENT_INFO', 'EQUIPMENT_INFO', 'ERATE_INFO', 'EVALUATE_CATALOG', 'EVALUATE_DATA',
           'EVALUATE_MODEL', 'EVALUATE_RECORD', 'EXAMPLE_DATAWINDOW', 'EXAMPLE_INFO', 'FINANCE_ITEM',
           'FINANCEBUSINESS_APPLY', 'FLOW_CATALOG', 'FLOW_MODEL', 'FLOW_MODEL_HIS', 'FLOW_OBJECT', 'FLOW_OPINION',
           'FLOW_SWIMLANE', 'FLOW_TASK', 'FORMATDOC_CATALOG', 'FORMATDOC_DEF', 'FORMATDOC_PARA', 'GCI4XD_SETUP',
           'GOVERNMENT_INFO', 'GROUP_CHANGE', 'GROUP_RELATIVE', 'GROUP_RESULT', 'GROUP_SEARCH', 'GROUPTASK_FLOW',
           'GUARANTY_INFO_LSCK', 'GUARANTY_TRANSFORM', 'IMPORT_DATA_INFO', 'IND_EDUCATION', 'IND_INFO', 'INIT_SERIALNO',
           'INSPECT_INFO', 'INSPECT_REPORT_XJ_MX', 'INSPECT_REPORT_XJ_TJ', 'INTERACTION_LOG', 'KNOWLEDGE_CATALOG',
           'KNOWLEDGE_OBJECT', 'LC_INFO', 'LOANHANDOVER', 'LOANOUT', 'LOG_AUDITINFO', 'MAINFRAMEORG_INFO',
           'MAINFRAMEORG_RELA', 'MANAGE_CHANGE', 'OBJECT_MAXSN', 'OBJECTTYPE_CATALOG', 'OBJECTTYPE_RELA', 'ORG_BELONG',
           'ORG_COMPARE', 'ORG_INFO', 'OSF_LOG', 'OSFCLIENT_LOG', 'PARA_CONFIGURE', 'PARAMENT_LIBRARY',
           'PARAMET_CALCULATE', 'PARTNER_PROJECT_CHANGE_INFO', 'PARTNER_PROJECT_INFO', 'PLANCHANGE', 'PRD_NODECONFIG',
           'PRD_NODEINFO', 'PRINT_CONT', 'PRODUCT_TERM_LIBRARY', 'PRODUCT_TERM_PARA', 'PRODUCT_TERM_RELATIVE',
           'PRODUCT_VERSION', 'PROJECT_ADJUST_HISTORY', 'PROJECT_ASSET_RELA', 'PROJECT_BAIL_INFO', 'PROJECT_BUDGET',
           'PROJECT_BUYBACK', 'PROJECT_CONSIGNER_INFO', 'PROJECT_FUNDS', 'PROJECT_INFO', 'PROJECT_PROGRESS',
           'PROJECT_RELATIVE', 'RATE_INFO_HIS', 'RATE_INFO_LOG', 'RC_CH_INFO', 'RECLAIM_INFO', 'RECORD_UUID',
           'REINFORCE_ACCOUNT', 'REPORT_CATALOG', 'REPORT_DATA', 'REPORT_MODEL', 'REPORT_RECORD', 'RESERVE_ENTPARA',
           'RESERVE_INDPARA', 'RIGHT_INFO', 'ROLE_RIGHT', 'RT_INTERFACE_LOG', 'SADRE_ASSUMPTION', 'SADRE_DIMENSION',
           'SADRE_RULESCENE', 'SADRE_RUNNING_LOG', 'SADRE_SCENEGROUP', 'SADRE_SCENERELATIVE', 'SADRE_SYNONYMN',
           'SALEACCEPT_CUSTOMER_INFO', 'SCENARIO_ARGS', 'SCENARIO_CATALOG', 'SCENARIO_GROUP', 'SCENARIO_MODEL',
           'SCENARIO_RELATIVE', 'SECURITY_AUDIT', 'SELECT_CATALOG', 'SME_APPLY', 'SME_CONFMODE', 'SME_CONSINFO',
           'SME_CUSTACCO', 'SME_CUSTRELA', 'SME_INVEINFO', 'STATISTIC_PARAMS', 'SUBJECT_INFO', 'SYSTEM_CHANGE_CONTEXT',
           'SYSTEM_CHANGE_LOG', 'SYSTEM_SETUP', 'T_1', 'TABLE_INFO', 'TABLECOL_INFO', 'TEMP_ENTINFO', 'TEST_AA',
           'TRADE_CATALOG', 'TRADE_CLIENT_LOG', 'TRADE_SERVICE_LOG', 'TRANS_DETAIL', 'TRANS_ENTRY', 'TRANSACTION_LOG',
           'TRANSFER_JOIN_ORGS', 'USER_DEFINEINFO', 'USER_FAILEDLIST', 'USER_INFO', 'USER_LIST', 'USER_MARKINFO',
           'USER_PASSWORD_HISTORY', 'USER_RIGHT', 'USER_ROLE', 'USERFINAL_PUTOUT', 'VEHICLE_INFO', 'VEHICLE_RELATIVE',
           'WATERCRAFT_INFO']
table_l = ['ENT_BONDISSUE', 'ENT_IPO', 'ACCOUNTENTRY', 'ACCOUNTING_CATALOG', 'ACCOUNTING_LIBRARY', 'ACCTFLOW_TEMP_HIS',
           'ACCT_BUSINESS_SUBJECT_MAPPING', 'ACCT_BUSINESS_SUBJECT_RULE', 'ACCT_CORE_ACCOUNT', 'ACCT_DEPOSIT_ACCOUNTS',
           'ACCT_FEE', 'ACCT_FEE_LOG', 'ACCT_FILE_NAME', 'ACCT_GENERAL_LEDGER', 'ACCT_GENERAL_LEDGER_HIS',
           'ACCT_INTEREST_LOG', 'ACCT_LOAN', 'ACCT_LOAN_BALANCE', 'ACCT_LOAN_CHANGE', 'ACCT_LOAN_QUERY',
           'ACCT_PAYMENT_LOG', 'ACCT_PAYMENT_SCHEDULE', 'ACCT_PAYMENT_SCHEDULE_BACKUP', 'ACCT_RATE_SEGMENT',
           'ACCT_RATE_SEGMENT_BACKUP', 'ACCT_RPT_SEGMENT', 'ACCT_SPT_SEGMENT', 'ACCT_SUBJECT_MAPPING',
           'ACCT_SUBLEDGER_DETAIL', 'ACCT_SUBSIDIARY_LEDGER', 'ACCT_SUBSIDIARY_LEDGER_HIS',
           'ACCT_SUBSIDIARY_LEDGER_MONTH', 'ACCT_TEMP', 'ACCT_TEMP_HIS', 'ACCT_TRANSACTION', 'ACCT_TRANSFER',
           'ACCT_TRANS_ASSETSALE', 'ACCT_TRANS_PAYMENT', 'ACCT_TRANS_WRITEOFF', 'ACCT_WORK_REGISTER', 'AFTERLOAN18',
           'AFTERLOAN20', 'AFTERLOAN23', 'AFTERLOAN24', 'AFTERLOAN25', 'AFTERLOAN26', 'AFTERLOAN27', 'AFTERLOAN29',
           'AFTERLOAN30', 'AGENCY_INFO', 'AGENT_INFO', 'ALSREPORT_WEB', 'ALS_DESIGN', 'ALS_TABLE', 'ALS_TABLE_METADATA',
           'ALS_TABLE_PERFORMANCE', 'ALS_TABLE_RELATIVE', 'APPLY_RELATIVE', 'APPROVE_DATA', 'APPROVE_DATA_TEMP',
           'APPROVE_RELATIVE', 'AREA_LIBRARY', 'ASSETWARD_INFO', 'ASSET_BALANCE', 'ASSET_CONTRACT', 'ASSET_DISPOSITION',
           'ASSET_INFO', 'ASSET_RANSOM', 'ASYNC_TASK_RECORD', 'AUDIT_INFO', 'AWE_DICT_ERRMSG', 'AWE_DO_CATALOG',
           'AWE_DO_COL_VALIDATE', 'AWE_DO_EVENT', 'AWE_DO_GROUP', 'AWE_DO_LIBRARY', 'AWE_DO_MODES', 'AWE_DO_VALIDATE',
           'AWE_DO_VALIDATE_CATALOG', 'AWE_DW_CONTEXT', 'AWE_ERPT_CATALOG', 'AWE_ERPT_DATA', 'AWE_ERPT_DEF',
           'AWE_ERPT_MAP', 'AWE_ERPT_OFFLINE', 'AWE_ERPT_RECORD', 'AWE_ERPT_TYPE', 'AWE_FUNCTION_INFO',
           'AWE_GROUP_CATALOG', 'AWE_GROUP_CLASSIFY', 'AWE_GROUP_ITEM', 'AWE_HREF_INFO', 'AWE_JSP_RUNTIME',
           'AWE_MENU_INFO', 'AWE_QUICK_HREF', 'AWE_ROLE_FUNCTION', 'AWE_ROLE_INFO', 'AWE_ROLE_MENU', 'AWE_TASK_INFO',
           'BATCHSN', 'BATCH_ACCOUNTNO_TRANSACTION', 'BATCH_ACCOUNT_DATA', 'BATCH_ACCOUNT_INFO', 'BATCH_CORE_LAS',
           'BATCH_CREDITINQUIRY_MESSAGE', 'BATCH_DCZY_LOAN_INFO', 'BATCH_DC_LIST', 'BATCH_DC_PRICE',
           'BATCH_DEDUCT_INFO', 'BATCH_DEDUCT_INFO_HISTORY', 'BATCH_FILE_MESSAGE', 'BATCH_LAS_CORE',
           'BATCH_MIDDLEACCOUNT_INFO', 'BATCH_NOTE_MESSAGE', 'BATCH_OFFBSADVANCE_INFO', 'BATCH_SUBJECTLEDGER_INFO',
           'BATCH_TASKERROR', 'BATCH_TASKSTATUS', 'BATCH_TRANSFER_INFO', 'BATCH_TRANSFER_LIST', 'BFJFLOW_TEMP_HIS',
           'BFJSUM_TEMP', 'BFJSUM_TEMP_HIS', 'BILL_GUIDEINTERESTRATE', 'BILL_GUIDERATE_PACKAGE', 'BILL_INFO',
           'BOARD_LIST', 'BUILDING_DETAIL', 'BUILDING_INFO', 'BUSIINFO_TEMP_HIS', 'BUSINESSARG_FUNCTIONNO',
           'BUSINESSTYPE_ARG', 'BUSINESSTYPE_CHANGE_TEMP', 'BUSINESSTYPE_COMPARE', 'BUSINESSTYPE_LIMIT',
           'BUSINESS_APPLICANT', 'BUSINESS_APPLY', 'BUSINESS_APPROVE', 'BUSINESS_CONTRACT', 'BUSINESS_CONTRACT_NO_BOOK',
           'BUSINESS_DUEBILL', 'BUSINESS_HISTORY', 'BUSINESS_LOANCOUNT', 'BUSINESS_PROVIDER', 'BUSINESS_PUTOUT',
           'BUSINESS_RECEIPT', 'BUSINESS_SORT', 'BUSINESS_TYPE', 'BUSINESS_WASTEBOOK', 'CALENDAR_WORK',
           'CARINFO_TEMP_HIS', 'CASHFLOW_DATA', 'CASHFLOW_PARAMETER', 'CASHFLOW_RECORD', 'CLASSIFYDUEBILL_BLACK',
           'CLASSIFY_CATALOG', 'CLASSIFY_DATA', 'CLASSIFY_MODEL', 'CLASSIFY_RECORD', 'CLASS_CATALOG', 'CLASS_METHOD',
           'CL_DIVIDE', 'CL_ERROR_TYPE', 'CL_INFO', 'CL_INFO2', 'CL_INFO_LOG', 'CL_LIMITATION_TYPE', 'CL_OCCUPY',
           'CL_TEAM', 'CL_TYPE', 'CL_USERULE', 'CMS_CERTMANAGE_INFO', 'CMS_CERTMANAGE_INFO_OLD', 'CMS_CHANGE_LOG',
           'CMS_COLLATERALDONO_INFO', 'CMS_COLLATERALTYPE_INFO', 'CMS_COLPOLICY_INFO', 'CMS_COLTYPE_EVAMOD',
           'CMS_COLTYPE_ORG', 'CMS_COL_PARAM', 'CODE_CATALOG', 'CODE_INFO', 'CODE_LIBRARY', 'CODE_TEMP', 'CONCEDE_INFO',
           'CONDITION_RULE', 'CONTRACT_RELATIVE', 'CORE_ASSETSALE', 'CORE_BILL_INFOA', 'CORE_BILL_INFOB',
           'CORE_BILL_INFOC', 'CORE_DEPOSIT_ACCOUNTS', 'CORE_DETAIL', 'CORE_LOAN', 'CORE_PAYMENT_LOG1',
           'CORE_PAYMENT_LOG2', 'CORE_RATE_SEGMENT', 'CORE_RCPFD', 'CORE_SPT_DETAIL', 'CORE_SPT_SEGMENT',
           'CORE_SUBSIDIARY_LEDGER', 'CORE_TRANS_PAYMENT', 'CORE_TRANS_PAYMENT1', 'CORE_TRANS_PAYMENT2', 'COST_INFO',
           'CREDITINQUIRY_APPLY', 'CREDITINQUIRY_ORG', 'CREDITINQUIRY_RELATIVE', 'CREDITINQUIRY_USER',
           'CREDITLINE_RELA', 'CREDITUSEINFO', 'CREDIT_INFO_TEMP_HIS', 'CRQ_ACCOUNT', 'CRQ_PARA', 'CUSTOMER_ADDRESS',
           'CUSTOMER_ANARECORD', 'CUSTOMER_BELONG', 'CUSTOMER_BOND', 'CUSTOMER_CERT', 'CUSTOMER_ECR_RECORD',
           'CUSTOMER_FSRECORD', 'CUSTOMER_IMASSET', 'CUSTOMER_IMPORT_LOG', 'CUSTOMER_INFO', 'CUSTOMER_INFO_CHANGE',
           'CUSTOMER_INFO_TEMP_HIS', 'CUSTOMER_MEMO', 'CUSTOMER_MERGE', 'CUSTOMER_MODEL', 'CUSTOMER_OACTIVITY',
           'CUSTOMER_PARTNER', 'CUSTOMER_REALTY', 'CUSTOMER_RELATIVE', 'CUSTOMER_SPECIAL', 'CUSTOMER_TAXPAYING',
           'CUSTOMER_TEL', 'CUSTOMER_TRANSFER', 'CUSTOMER_VEHICLE', 'DATAOBJECT_CATALOG', 'DATAOBJECT_COL_VALID',
           'DATAOBJECT_GROUP', 'DATAOBJECT_LIBRARY', 'DBEXTENSION', 'DCZY_GUARANTY_AUDIT', 'DCZY_PRODUCT_INFO',
           'DCZY_RELATIVE_INFO', 'DCZY_TRADE_CONSTANS', 'DEPOSIT_TEMP', 'DOCUMENT_CATALOG', 'DOCUMENT_DATA',
           'DOCUMENT_LIBRARY', 'DOCUMENT_RECORD', 'DOC_ATTACHMENT', 'DOC_ATTACHMENT_TASK', 'DOC_LIBRARY',
           'DOC_RELATIVE', 'DS_SIGHT', 'DS_SIGHT_SET', 'DUEBILLEXTENSION', 'DUN_INFO', 'DUTY_INFO', 'DWTEMPLATE_INFO',
           'ECM_IMAGE_TYPE', 'ECM_PRDIMAGE_RELA', 'ENTRUST_INFO', 'ENT_AUTH', 'ENT_FIXEDASSETS', 'ENT_FOA', 'ENT_INFO',
           'ENT_INVENTORY', 'ENT_REALTYAUTH', 'EQUIPMENT_INFO', 'ERATE_INFO', 'ERROR_TEMP', 'EVALUATE_CATALOG',
           'EVALUATE_DATA', 'EVALUATE_INFO', 'EVALUATE_MODEL', 'EVALUATE_RECORD', 'EXAMPLE_DATAWINDOW', 'EXAMPLE_INFO',
           'FILENUM_TEMP', 'FILENUM_TEMP_HIS', 'FINANCEBUSINESS_APPLY', 'FINANCE_ITEM', 'FLOW_CATALOG', 'FLOW_MODEL',
           'FLOW_OBJECT', 'FLOW_OPINION', 'FLOW_RECORD', 'FLOW_TASK', 'FORMATDOC_CATALOG', 'FORMATDOC_DATA',
           'FORMATDOC_DEF', 'FORMATDOC_PARA', 'FORMATDOC_RECORD', 'GCI4XD_SETUP', 'GLINE_INFO', 'GOVERNMENT_INFO',
           'GREENWAY_INFO', 'GROUPTASK_FLOW', 'GROUP_RESULT', 'GROUP_SEARCH', 'GUARANTY_ADDRECORD',
           'GUARANTY_ADDRECORD_LOG', 'GUARANTY_APPLY', 'GUARANTY_AUDIT', 'GUARANTY_CONTRACT', 'GUARANTY_CONTRACT_OLD',
           'GUARANTY_INFO', 'GUARANTY_INFO_OLD', 'GUARANTY_RELATION', 'GUARANTY_RELATIVE', 'GUARANTY_RELATIVE_OLD',
           'GUARANTY_TRANSFORM', 'HR_EMP_INFO', 'HR_ORGINFO_FULL', 'IND_EDUCATION', 'IND_INFO', 'IND_RESUME',
           'INSPECT_CONFIG', 'INSPECT_DATA', 'INSPECT_DETAIL', 'INSPECT_INFO', 'INSPECT_LOAN_INFO',
           'INSPECT_REPORT_XJ_MX', 'INTERACTION_LOG', 'INTERBILLTX_RELATIVE', 'INTERCOURSEACCOUNT_CHECK',
           'INVOICE_BILL', 'JCPF10', 'KNOWLEDGE_CATALOG', 'KNOWLEDGE_OBJECT', 'LAWCASE_INFO', 'LAWCASE_PERSONS',
           'LC_INFO', 'LIMIT_INFO', 'LOANCHECK', 'LOANCHECKAPP', 'LOANDETAIL_TEMP_HIS', 'LOANHANDOVER', 'LOANOUT',
           'LOANSORT', 'LOANSORT2', 'LOANTEMP_PUTOUT_RELATIVE', 'LOAN_DIRECTION', 'LOG_AUDITINFO', 'LPR_CHANGE_RECORD',
           'MAINFRAMEORG_INFO', 'MAINFRAMEORG_RELA', 'MANAGE_CHANGE', 'MFCUSTOMER_RELATIVE', 'MOVABLE_PROPERTY_INFO',
           'NW_ERROR_LOG', 'OBJECTTYPE_CATALOG', 'OBJECTTYPE_RELA', 'OBJECT_MAXSN', 'ORG_COMPARE', 'ORG_INFO',
           'OSFCLIENT_LOG', 'OSF_LOG', 'OTHERCHANGE_INFO', 'OTHER_RELATIVE', 'PARAMENT_LIBRARY', 'PARAMET_CALCULATE',
           'PARA_CONFIGURE', 'PARTNER_PROJECT_ASSETDEAL', 'PARTNER_PROJECT_CHANGE_INFO', 'PARTNER_PROJECT_INFO',
           'PARTNER_PROJECT_INSURANCE', 'PARTNER_PROJECT_RELATIVE', 'PAYLOG_TEMP_HIS', 'PAYMENT_INFO',
           'PAYMENT_SCHEDULE', 'PAYPLAN_TEMP_HIS', 'PLANCHANGE', 'PRD_NODECONFIG', 'PRD_NODEINFO', 'PRINT_CONT',
           'PRINT_DATA', 'PRINT_RELATIVE_DATA', 'PRODUCT_TERM_LIBRARY', 'PRODUCT_TERM_PARA', 'PRODUCT_TERM_RELATIVE',
           'PRODUCT_VERSION', 'PROJECT_ADJUST_HISTORY', 'PROJECT_ASSET_RELA', 'PROJECT_BAIL_INFO', 'PROJECT_BUDGET',
           'PROJECT_BUYBACK', 'PROJECT_CONSIGNER_INFO', 'PROJECT_FUNDS', 'PROJECT_INFO', 'PROJECT_PROGRESS',
           'PROJECT_RELATIVE', 'RATE_BATCH_EXCEL', 'RATE_BATCH_LIST', 'RATE_INFO', 'RATE_INFO_HIS', 'RATE_INFO_LOG',
           'RCPF26', 'RCPF28', 'RCPF81', 'RC_CH_INFO', 'REALTY_RELATIVE', 'RECLAIM_INFO', 'REINFORCE_ACCOUNT',
           'REPORT_CATALOG', 'REPORT_DATA', 'REPORT_MODEL', 'REPORT_RECORD', 'RESERVE_ENTPARA', 'RESERVE_INDPARA',
           'RESERVE_PREDICTDATA', 'REVTRANS_TEMP_HIS', 'RIGHT_INFO', 'RISKSIGNAL_OPINION', 'RISK_SIGNAL', 'ROLE_RIGHT',
           'RT_INTERFACE_LOG', 'SADRE_ASSUMPTION', 'SADRE_DIMENSION', 'SADRE_RULESCENE', 'SADRE_RUNNING_LOG',
           'SADRE_SCENEGROUP', 'SADRE_SCENERELATIVE', 'SADRE_SYNONYMN', 'SALEACCEPT_CUSTOMER_INFO', 'SCENARIO_ARGS',
           'SCENARIO_CATALOG', 'SCENARIO_GROUP', 'SCENARIO_MODEL', 'SCENARIO_RELATIVE', 'SECURITYIN', 'SECURITYOUT',
           'SECURITY_AUDIT', 'SELECT_CATALOG', 'SME_APPLY', 'SME_CONFMODE', 'SME_CONSINFO', 'SME_CUSTACCO',
           'SME_CUSTRELA', 'SME_INVEINFO', 'SPECIALBUSINESS_TEMP_HIS', 'STATISTIC_INFO', 'STATISTIC_PARAMS',
           'SUBJECT_INFO', 'SYSTEM_CHANGE_CONTEXT', 'SYSTEM_CHANGE_LOG', 'SYSTEM_SETUP', 'TABLECOL_INFO', 'TABLE_INFO',
           'TEMP_BUSINESS_DUEBILL', 'TEMP_CUSTOMERRELATIVE', 'TEMP_ENTINFO', 'TEMP_INDINFO', 'TEST_AA', 'TIMEING_TASK',
           'TRADE_CATALOG', 'TRADE_CLIENT_LOG', 'TRADE_SERVICE_LOG', 'TRANSFER_JOIN_ORGS', 'TRANSFORM_RELATIVE',
           'TRANS_DEPOSIT_ACCOUNTS', 'TRANS_DETAIL', 'TRANS_ENTRY', 'TRANS_LOAN', 'TRANS_PAYMENT_LOG',
           'TRANS_PAYMENT_SCHEDULE', 'TRANS_RATE_SEGMENT', 'TRANS_RPT_SEGMENT', 'TRANS_SPT_SEGMENT',
           'TRANS_SUBSIDIARY_LEDGER', 'T_1', 'USER_DEFINEINFO', 'USER_FAILEDLIST', 'USER_INFO', 'USER_LIST',
           'USER_MAPPING', 'USER_MARKINFO', 'USER_PASSWORD_HISTORY', 'USER_ROLE', 'VEHICLE_INFO', 'VEHICLE_RELATIVE',
           'VM_BUSINESS_DUEBILL', 'WATERCRAFT_INFO', 'WEBSERVICE_LOG', 'WORK_RECORD']
table_p = ['ACCOUNTDAY_INFO', 'ACCOUNT_INFO_TEMP', 'ADMINOPERATION_AUTHORIZATION', 'ALS_INDUCODEMAP',
           'ALS_UPDATEBUSIINDUSTRY', 'ALS_UPDATEENTINDUSTRY', 'ANALYST_INFO_RATIO', 'APPLY_CERTIFICATE',
           'ARCHIVES_BORROW', 'ARCHIVES_DESTRUCT', 'APPLY_RELATIVE', 'APPROVE_DATA', 'ARCHIVES_TRANSFER',
           'ARTIFICIALNO_BACKUP', 'ASSESS_RECORD', 'ASSET_BALANCE', 'ASSET_CONTRACT', 'ASSET_DISPOSITION',
           'ASYNC_TASK_RECORD', 'AUDIT_INFO', 'AUTHORIZE_METHOD', 'AUTHORIZE_OBJECT', 'AUTHORIZE_ORG', 'AUTHORIZE_ROLE',
           'AWE_DICT_ERRMSG', 'AWE_DO_CATALOG', 'AWE_DO_EVENT', 'AWE_DO_GROUP', 'AWE_DO_LIBRARY', 'AWE_DO_MODES',
           'AWE_DO_VALIDATE', 'AWE_DO_VALIDATE_CATALOG', 'AWE_ERPT_CATALOG', 'AWE_ERPT_DEF', 'AWE_ERPT_MAP',
           'AWE_ERPT_PARA', 'AWE_ERPT_TYPE', 'AWE_HREF_INFO', 'AWE_JSP_RUNTIME', 'AWE_MENU_INFO', 'AWE_ROLE_MENU',
           'AWE_ROLE_URL', 'BANK_INFO', 'BATCH_CTRL', 'BATCH_TRANSFER_INFO', 'BATCH_TRANSFER_LIST', 'BILLUSER_INFO',
           'BATCH_CREDITINQUIRY_MESSAGE', 'BILL_INFO_HIS', 'BILL_INFO_TEMP', 'BOARD_LIST', 'BUSINESS_EXTENSION',
           'BUSINESS_SORT', 'BUSINESS_SORTNO', 'BILL_INFO', 'CALENDAR_WORK', 'CLASSIFY_CATALOG', 'CLASSIFY_CHANGE',
           'BOND_INFO', 'BUILDING_INFO', 'BUSINESS_APPLICANT', 'BUSINESS_APPLY', 'BUSINESS_APPLY_REPORT',
           'CLASSIFY_DATA', 'BUSINESS_CONTRACT', 'BUSINESS_DUEBILL', 'CLASSIFY_MODEL', 'CLASS_CATALOG',
           'BUSINESS_PUTOUT', 'CLASS_METHOD', 'CL_ERROR_TYPE', 'CL_INFO_LOG', 'CL_LIMITATION_TYPE', 'CL_TYPE',
           'CNAPSBANKINFO', 'CODE_CATALOG', 'CODE_LIBRARY', 'CODE_LIBRARY2', 'CONTRACT_RELATIVE_LOG', 'COST_INFO',
           'CREDITINQUIRY_ORG', 'CREDITINQUIRY_USER', 'CREDITSCOPE_INFO', 'CUSTOMERBELONG_APPLY', 'CUSTOMER_IMPORT_LOG',
           'CUSTOMER_INFO_CHANGE', 'CUSTOMER_INFO_TEMP', 'CUSTOMER_TRANSFER', 'DATAOBJECT_CATALOG', 'DATAOBJECT_GROUP',
           'DATAOBJECT_LIBRARY', 'DHCREDITSUM', 'DHCREDITSUM2', 'CONTRACT_RELATIVE', 'DOC_ATTACHMENT_TASK',
           'DUEBILL_BALANCE_RECORD', 'CREDITINQUIRY_APPLY', 'ECM_IMAGE_TYPE', 'CREDITINQUIRY_RELATIVE',
           'ECM_PRDIMAGE_RELA', 'ELCSBUSINESSINFO_IMPORT', 'ENT_INFO_C', 'ENT_INFO_CHANGE', 'ENT_INFO_V', 'ERATE_INFO',
           'EVALUATE_CATALOG', 'EVALUATE_DATA', 'CUSTOMER_BELONG', 'EVALUATE_INFO', 'EVALUATE_MODEL', 'FAMILY_EXPENSES',
           'CUSTOMER_INFO', 'FILE_INFO', 'FINANCE_ITEM', 'FLOW_CATALOG', 'CUSTOMER_MEMO', 'CUSTOMER_OACTIVITY',
           'CUSTOMER_REALTY', 'CUSTOMER_RELATIVE', 'CUSTOMER_SPECIAL', 'FLOW_LOG', 'CUSTOMER_VEHICLE', 'FLOW_MODEL',
           'FORMATDOC_CATALOG', 'FORMATDOC_DEF', 'FORMATDOC_PARA', 'F_TX_TRANS_INFO_MID', 'DOC_ATTACHMENT',
           'GJFOREIGNRATE', 'DOC_LIBRARY', 'DOC_RELATIVE', 'GOVERNMENT_INFO', 'GROUPTASK_FLOW', 'GROUP_EVENT',
           'GROUP_FAMILY_VERSION', 'GUARANTEECOMPANY', 'ECM_PAGE', 'GUARANTY_AUDIT', 'GUARANTY_CONTRACT_BAK',
           'ENT_AUTH', 'ENT_BONDISSUE', 'ENT_ENTRANCEAUTH', 'ENT_FIXEDASSETS', 'ENT_INFO', 'GUARANTY_LIMIT',
           'GUARANTY_TRANSFORM', 'GYLTRANS_RECORD', 'ENT_IPO', 'HOUSEVALUE_RECORD', 'HR_EMP_INFO', 'HR_ORGINFO_FULL',
           'ICR_EXTENDINFO', 'ICR_EXTSPECBUSI', 'IND_INFO_CHANGE', 'INIT_SERIALNO', 'INSPECT_CONFIG',
           'INSPECT_CONFIG_CHANGE', 'LOANBACKSTATUS', 'LOG_AUDITINFO', 'MAKE_GUARANTEE_SEQNO', 'MANAGER_CHECKREPORT',
           'MANAGE_CHANGE', 'META_DATABASE', 'MFENT_INFO', 'M_RPT_UN_ACQ_MRCH_COST_MON', 'NC_GUARANTEE_TRANS',
           'OBJECTTYPE_CATALOG', 'OBJECTTYPE_RELA', 'FPDEMO', 'OBJECT_LEVEL', 'OBJECT_MAXSN', 'ODS_UNITESIGN_INFO',
           'ONLINE_BUSINESS_INFO', 'ONLINE_CUSTOMER_LIMIT', 'ONLINE_LOCK_CUSTOMER', 'ONLINE_MSG_LOG', 'ONLINE_OSF_LOG',
           'ONLINE_PRODUCT_CONFIG', 'ONLINE_PRODUCT_INFO', 'GUARANTY_CONTRACT', 'ORGIP_INFO', 'GUARANTY_INFO',
           'GUARANTY_INFO_LSCK', 'OSFCLIENT_LOG', 'GUARANTY_RELATIVE', 'GUARANTY_RIGHT', 'OSF_LOG', 'OTHERCHANGE_INFO',
           'PARA_CONFIGURE', 'PBCATEDT', 'PBCATFMT', 'PH_BUSINESS_MAPPING', 'PH_EXISTS_CONTRACT', 'IND_EDUCATION',
           'IND_INFO', 'PRO_MAKE_PRICE', 'IND_RESUME', 'RATETYPECHANGE', 'RATE_TYPE_CHANGE', 'REALTYAPPTINFO',
           'RECCUSTOMER_NOPASS', 'RECORD_UUID', 'REG_APP_DEF', 'REG_COMMENT_ITEM', 'REG_COMMENT_RELA', 'REG_COMP_DEF',
           'REG_COMP_PAGE', 'REG_DBCONN_DEF', 'REG_FUNCTION_DEF', 'REG_PAGE_DEF', 'REINFORCE_ACCOUNT', 'REPORT_CATALOG',
           'REPORT_MODEL', 'RIGHT_INFO', 'RISK_SIGNAL', 'ROLE_RIGHT', 'RT_INTERFACE_LOG', 'SCENARIO_ARGS',
           'SCENARIO_CATALOG', 'SCENARIO_GROUP', 'SCENARIO_MODEL', 'SCENARIO_RELATIVE', 'SECURITY_AUDIT',
           'SELECT_CATALOG', 'SME_CONFMODE', 'SQL_RUNTIME', 'STATISTIC_INFO', 'STATISTIC_PARAMS', 'SUBJECT_HISTORY',
           'SUBJECT_INFO', 'SYSTEM_LOG', 'SYSTEM_MENU', 'SY_APPLY_INFO', 'SY_CUSTOMER_INFO', 'TASK_LOG',
           'TASK_POLLING_RUNLOG', 'TD_QUERY_HISTORY', 'TEMP1', 'TEST_RECORD', 'TIME_CONTROL', 'TRANSACTION_INFO',
           'TRANSACTION_INFO_PJ', 'PAYMENT_INFO', 'TRANSFORM_RELATIVE', 'TRANS_LOG', 'USER_AUTHORIZATION',
           'USER_DEFINEINFO', 'USER_FAILEDLIST', 'USER_LIST', 'USER_MAPPING', 'USER_MARKINFO', 'USER_PASSWORD_HISTORY',
           'USER_PREF', 'USER_ROLE', 'USER_RUNTIME', 'PROJECT_RELATIVE', 'VM_BUSINESS_DUEBILL', 'PUTOUT_RELATIVE',
           'WITHHOLDING_INFO', 'RATE_TYPE', 'WORK_RECORD', 'XD_SERVICE_LOG', 'ADDITION_INFO', 'ANALYST_INFO',
           'ASSETSSOLD_APPLY', 'AWE_ROLE_INFO', 'BATCH_MESSAGE_NOTE', 'BC_BUSINESS_PUTOUT', 'BUSINESS_CARD',
           'BUSINESS_HISTORY', 'BUSINESS_TYPE', 'BUSINESS_WASTEBOOK', 'CASHFLOW_DATA', 'CASHFLOW_PARAMETER',
           'CASHFLOW_RECORD', 'REPAYMENTSCHEDULE', 'CLASSIFY_RECORD', 'CL_INFO', 'CREDITLINE_RELA', 'CREDITORG_LIMIT',
           'CREDIT_DEDUCT', 'CUSTOMERINFO_LS', 'CUSTOMER_ANARECORD', 'CUSTOMER_ELOAN', 'CUSTOMER_FSRECORD',
           'CUSTOMER_INSPECT_INFO', 'DUEBILL_PURPOSE_CHECK', 'DUEBILL_PURPOSE_LIST', 'DUN_INFO', 'EVALUATE_RECORD',
           'FLOW_OBJECT', 'FLOW_OPINION', 'FLOW_TASK', 'FORMATDOC_DATA', 'FORMATDOC_RECORD', 'FUNDBUSINESS_APPLY',
           'SME_CUSTRELA', 'GROUP_INFO', 'INSPECT_DATA', 'INSPECT_DETAIL', 'INSPECT_INFO', 'INSPECT_LOAN_INFO',
           'INSPECT_REPORT_XJ_MX', 'MANGO_APPLY_INFO', 'MANGO_CUSTOMER_INFO', 'MARKETPRODUCT_INFO',
           'MARKETPRODUCT_RELA', 'NC_GUARANTEE_INFO', 'ONLINE_APPLY_INFO', 'ONLINE_ORDER_RECORD', 'ORG_INFO',
           'PARTNER_PROJECT_CHANGE_INFO', 'PARTNER_PROJECT_INFO', 'PARTNER_PROJECT_RELATIVE', 'PREPARE_APPROVE_INFO',
           'PRESALEFUNDS', 'PRINT_DATA', 'PRINT_RELATIVE_DATA', 'PROJECT_BUDGET', 'PROJECT_FUNDS', 'PROJECT_INFO',
           'PROJECT_PROGRESS', 'REALTYINFO', 'RECOMMENDUSER_INFO', 'REPAYMENT_RECORD', 'REPORT_DATA', 'REPORT_RECORD',
           'ROLE_INFO', 'SME_CONSINFO', 'SME_CUSTACCO', 'SY_REPAY_INFO', 'UNION_GUARANTY_MEMBER',
           'UNION_MEMBER_RELATIVE', 'USER_INFO']


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


# 创建一个函数，参数可以是任意多个文件路径，根据传入文件路径，删除文件
def del_file(*file_path):
    for file in file_path:
        if os.path.exists(file):
            print("文件：", file, " 要在关闭状态才能删除重建哦！！")
            # 如果文件存在，则删除它
            os.remove(file)
            print(f"文件 {file} 已删除。")
        else:
            print(f"文件 {file} 不存在。")


def get_table_catch_sys(sys_flag, table_catch):
    if table_catch is None or table_catch == '':
        return table_catch
    table_catch = str(table_catch).upper()
    if sys_flag == FLAG_SYS_L:
        for table in table_l:
            table_catch = table_catch.replace(table, L_SCHEMA + table)
        return table_catch
    elif sys_flag == FLAG_SYS_S:
        for table in table_s:
            table_catch = table_catch.replace(table, S_SCHEMA + table)
        return table_catch
    elif sys_flag == FLAG_SYS_P:
        for table in table_p:
            table_catch = table_catch.replace(table, P_SCHEMA + table)
        return table_catch
    else:
        return "系统标识错误"


def init_pd_config(pd):
    # 设置显示完整的列
    pd.set_option('display.max_columns', None)
    # 设置显示完整的行
    pd.set_option('display.max_rows', None)
    pd.options.mode.copy_on_write = True
    return pd


def mulu_list(df_all):
    ml = ['表名', '用例条数']
    first_df = pd.DataFrame(columns=ml)
    for sheet_name, df_sheet in df_all.items():
        new_df = pd.DataFrame({'表名': sheet_name, '用例条数': len(df_sheet)}, index=[0])
        first_df = pd.concat([first_df, new_df], ignore_index=True)
    new_df = pd.DataFrame({'表名': '合计', '用例条数': first_df['用例条数'].sum()}, index=[0])
    first_df = pd.concat([first_df, new_df], ignore_index=True)
    df_all['目录'] = first_df
    return df_all


def concat_df(df_all):
    # df_all是字典，key是表名，value是dataframe
    merged_df = pd.DataFrame()
    for sheet_name in df_all.keys():
        if sheet_name in ('目录') or "Sheet" in sheet_name:
            continue
        # df = df_all[sheet_name]
        merged_df = pd.concat([merged_df,df_all[sheet_name]])

    return merged_df


# source_df,tar_df,返回tar_df
def fz(sdf, tdf, sys_flag):
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
    init_row_nm = 1
    sum_num = sdf[sdf.columns[col_num_hh_field]].notnull().sum()

    if re.match(r'[a-zA-Z]', sdf.columns[1][0]):
        tab_en = str(sdf.columns[1])
        tab_en_cn = str(sdf.columns[1]) + "-" + str(sdf.iloc[0, 1]) + "_2" + sys_flag
    else:
        tab_en = str(sdf.iloc[0, 1])
        tab_en_cn = str(sdf.iloc[0, 1]) + "-" + str(sdf.columns[1]) + "_2" + sys_flag
    for i in range(5):
        # sdf.loc[i + 3, sdf.columns[col_num_code_sql]]
        for index, column in enumerate(tdf.columns):
            if i == 1 and (sdf.loc[i + 3, sdf.columns[col_num_hh_field]] is None or sdf.loc[
                i + 3, sdf.columns[col_num_hh_field]] == ""):
                continue
            elif index == 0:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_hh_field]]
            elif index == 1:
                tdf.loc[i + init_row_nm, column] = tab_en_cn
            elif index == 2:
                # 字段约束检查
                if "必输字段不为空" in sdf.loc[i + 3, sdf.columns[col_num_hh_field]]:
                    tdf.loc[i + init_row_nm, column] = "字段约束检查"
                else:
                    tdf.loc[i + init_row_nm, column] = "汇总检查"
            elif index == 3:
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_hh_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
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
        init_row_nm += 5
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
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_ver_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
            elif index == 6:
                if sys_flag == FLAG_SYS_L:
                    sum_table_name = L_SCHEMA + tab_en
                elif sys_flag == FLAG_SYS_S:
                    sum_table_name = S_SCHEMA + tab_en
                elif sys_flag == FLAG_SYS_P:
                    sum_table_name = P_SCHEMA + tab_en
                else:
                    sum_table_name = tab_en
                tdf.loc[i + init_row_nm, column] = f"select count(1) as tcount from {sum_table_name}"
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
    init_row_nm += desc_nm
    ver_nm = sdf[sdf.columns[col_num_code_field]].notnull().sum()
    for i in range(desc_nm):
        for index, column in enumerate(tdf.columns):
            if i == 1 and (sdf.loc[i + 2, sdf.columns[col_num_code_field]] is None or sdf.loc[
                i + 2, sdf.columns[col_num_code_field]] == ""):
                continue
            elif index == 0:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_code_field]]
            elif index == 1:
                tdf.loc[i + init_row_nm, column] = tab_en_cn
            elif index == 2:
                tdf.loc[i + init_row_nm, column] = "数据落标检查"
            elif index == 3:
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
            elif index == 4:
                tdf.loc[i + init_row_nm, column] = sdf.loc[i + 3, sdf.columns[col_num_code_sql]]
            elif index == 5:
                tdf.loc[i + init_row_nm, column] = sys_flag + "信贷库"
            elif index == 6:
                if sys_flag == FLAG_SYS_L:
                    tdf.loc[i + init_row_nm, column] = "select 0 as tcount from \"SYSIBM\".DUAL"
                elif sys_flag == FLAG_SYS_S:
                    tdf.loc[i + init_row_nm, column] = "select 0 as tcount from \"SYSIBM\".DUAL"
                elif sys_flag == FLAG_SYS_P:
                    tdf.loc[i + init_row_nm, column] = "select 0 as tcount from DUAL"
                else:
                    tdf.loc[i + init_row_nm, column] = "select 0 as tcount from DUAL"
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
    # 删除空行
    tdf = tdf.dropna(axis=0, how='any')
    return tdf
