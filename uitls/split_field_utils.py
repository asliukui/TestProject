import os




rp_arr=['NOT NULL','']

# 获取同级目录
same_level_directory = os.path.dirname(os.path.abspath(__file__))
# 设置输出文件名，如果存在先就删除，文件打开状态无法删除
file_source = "date_in.sql"
file_out = "date_out.sql"
# FILE_URL_IN = os.path.join(same_level_directory, "xintou_dev.xlsx")
FILE_URL_IN = os.path.join(same_level_directory, file_source)
FILE_URL_OUT = os.path.join(same_level_directory, file_out)

#按照行读取文件并处理文件后写出

    # 读取文件
with open(FILE_URL_IN, 'r', encoding='utf-8') as f:
    # 读取文件所有行
    lines = f.readlines()
    # 定义一个空列表用来存储处理后的数据
    new_lines = []
    # 遍历所有行
    for line in lines:
        # 处理每一行数据
        if line is not None:
            new_line = line.strip().replace("\t", "").split(" ")[0]
            # 将处理后的数据添加到新列表中
            new_lines.append(new_line)
    print(','.join(new_lines))
        # 将处理后的数据写入文件
        # with open(FILE_URL_OUT, 'w', encoding='utf-8') as f:
        #     f.writelines(new_lines)