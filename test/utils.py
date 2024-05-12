in_code = """FS01-正常贷款
FS03-逾期
FS10-结清
FS11-冲正"""
result = [i.split('-')[0] for i in in_code.split()]
result = str(result).replace('[',"(")
result = str(result).replace(']', ")")
print("not in "+result)