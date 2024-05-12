import sys
#  码值分割
#   python spilt_str.py "你的参数"
#   python spilt_str.py "FS01-正常贷款 FS03-逾期 FS10-结清 FS11-冲正"



in_code=""
if len(sys.argv) > 1:
    param = sys.argv[1]
    in_code = param
else:
    print("没有传递参数")
    sys.exit()

# in_code = """FS01-正常贷款
# FS03-逾期
# FS10-结清
# FS11-冲正"""
if len(in_code) >0:
    result = [i.split('-')[0] for i in in_code.split()]
    result = str(result).replace('[',"(")
    result = str(result).replace(']', ")")
    print("not in "+result)
else:
    print("请输入参数: py spilt_str.py 参数")