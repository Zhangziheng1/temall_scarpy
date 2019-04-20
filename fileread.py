# Author : ziheng_wind
# Email : wn345361049@163.com
# github : https://github.com/Zhangziheng1/temall_scarpy
# -*- coding: utf-8 -*-

def fread(fliename):
    list_new = []
    with open(fliename,'r') as f:
        data = f.readlines()
    for line in data:
        lines = str(line).replace('\n','')
        list_new.append(lines)
    return list_new,len(list_new)

if __name__ == "__main__":
    pass