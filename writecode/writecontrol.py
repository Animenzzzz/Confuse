# -*- coding: utf-8 -*-
import codemodel
import os
import linecache
import randomvalue
import filemanager

#当前脚本工程的绝对路径
confuse_path = "/Users/animenzzz/GitCode/Confuse"
confuse_resource_path = f'{confuse_path}/resource'
system_func_path = f'{confuse_resource_path}/func_analysised/uikit_class_func.txt'
random_func_path = f'{confuse_resource_path}/random_func_create.txt'

m_h_num_min = 5
m_h_num_max = 10

file_level = input(f"垃圾文件个数(每个文件内包含{m_h_num_min}-{m_h_num_max}个函数)： 1. 10-20  2. 20-30  3. 30-40\n")
file_num = randomvalue.intvalue((int(file_level)*10),(int(file_level)*10+10))

xcodefile_path = input("工程文件路径\n")
xcodefile_name = os.path.basename(xcodefile_path)

system_funcfile = open(system_func_path,'r')
system_func_lengh = len(system_funcfile.readlines())
system_funcfile.close()

if os.path.exists(random_func_path):
    os.remove(random_func_path)

print(f'新建的文件个数：{str(file_num)}')
for index in range(0,file_num):
    new_file_dic = filemanager.create_h_m(f'{xcodefile_path}/{xcodefile_name}')
    h_file = new_file_dic["h_path"]
    m_file = new_file_dic["m_path"]

    # 函数个数
    func_num = randomvalue.intvalue(m_h_num_min,m_h_num_max)

    for ii in range(1,func_num):
        func_arr = []
        # 获取系统方法的字符串
        for i in range(1,3):
            random_row = randomvalue.intvalue(1,system_func_lengh)
            random_line = linecache.getline(system_func_path, random_row)
            func_arr.append(random_line)
        # 函数信息，包括返回类型、参数等
        func_dic = randomvalue.funccreate(random_func_path,3)
        # 函数声明（写进.h中）
        func_head_string = f'{codemodel.constom_func_head_model(func_dic)};'
        filemanager.writestring(h_file,func_head_string)
        # 函数实现（写进.m中）
        func_write_string = codemodel.func_model(1,1,1,func_arr,1,func_dic)
        filemanager.writestring(m_file,func_write_string)
