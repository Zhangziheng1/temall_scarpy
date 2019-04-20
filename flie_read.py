# -*- coding: utf-8 -*-

"""
因为要频繁的使用读取文件操作
为了代码的复用性
所以自己写了一个模块
"""

def F_read(fliename):
    F_list = []
    with open(str(fliename)+'.txt', 'r') as f:
        data = f.readlines()
    for line in data:
        lines = str(line).replace('\n','')
        F_list.append(lines)
    F_L_lenght = len(F_list)
    #获取读取文件的长度
    return F_list,F_L_lenght

if __name__ == "__main__":
    pass
