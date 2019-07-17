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
random_class_name_path = f'{confuse_resource_path}/random_class_name.txt'

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

if os.path.exists(random_class_name_path):
    os.remove(random_class_name_path)

print(f'新建的文件个数：{str(file_num)}')
for index in range(0,file_num):
    new_file_dic = filemanager.create_h_m(f'{xcodefile_path}/{xcodefile_name}',name=None)
    h_file = new_file_dic["h_path"]
    m_file = new_file_dic["m_path"]
    class_name = new_file_dic["class_name"]


    classfile = open(random_class_name_path,'a+')
    classfile.writelines(f'{class_name}\n')
    classfile.close()

    # 函数个数
    func_num = randomvalue.intvalue(m_h_num_min,m_h_num_max)

    for ii in range(1,func_num):
        func_arr = []
        # 获取系统方法的字符串
        for i in range(1,3):
            random_row = randomvalue.intvalue(1,system_func_lengh)
            random_line = linecache.getline(system_func_path, random_row)
            func_arr.append(random_line)
        # 创建随机函数并且写入txt文件，函数信息，包括返回类型、参数等
        func_dic = randomvalue.funccreate(random_func_path,3,class_name)
        # 函数声明（写进.h中）
        func_head_string = f'{codemodel.constom_func_head_model(func_dic)};'
        filemanager.writestring(h_file,func_head_string,line_num=None)
        # 函数实现（写进.m中）
        func_write_string = codemodel.func_model(1,1,1,func_arr,1,func_dic)
        filemanager.writestring(m_file,func_write_string,line_num=None)

# 调用所有垃圾方法的开关
print("创建控制开关")
call_all_name = "AnimenzzzAllCall"
filemanager.create_h_m(f'{xcodefile_path}/{xcodefile_name}',f'{call_all_name}')
filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.m',"- (void)callString{\n\n\n\n\n\n}\n",line_num=None)
random_func_file = open(random_func_path)
for line in random_func_file:
    call_string = codemodel.constom_func_call_model(line,1)
    funcdic = eval(line)
    filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.m',call_string,line_num=7)


total = 4
random_classfunc_file = open(random_class_name_path,"r")
for num,value in enumerate(random_classfunc_file):
    total = total+1
    name = str(value).replace('\n','')
    filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.h',f'#import \"{name}.h\"\n' ,line_num=1)
random_classfunc_file.close()

print(f'最后的行号：{total}')

filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.h',"\n- (void)callString;\n",line_num=total)