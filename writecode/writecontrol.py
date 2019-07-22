# -*- coding: utf-8 -*-
import codemodel
import os
import linecache
import randomvalue
import filemanager
import subprocess
import sys
import datetime

# 当前脚本工程的路径
confuse_path = f'{os.path.dirname(sys.path[0])}'
confuse_resource_path = f'{confuse_path}/resource'
system_func_path = f'{confuse_resource_path}/func_analysised/uikit_class_func.txt'
random_func_path = f'{confuse_resource_path}/random_func_create.txt'
random_class_name_path = f'{confuse_resource_path}/random_class_name.txt'
ruby_path = f'{confuse_path}/writecode/xcodeprojhelp.rb'

# 文件夹白名单
file_while_list = ["Base","LoginService","View"]

# 函数的数量最值
m_h_num_min = 5
m_h_num_max = 10


def main(argv):

    file_level = input(f"新建垃圾文件个数(每个文件内包含{m_h_num_min}-{m_h_num_max}个函数)： 0. 不新建  1. 10-20  2. 20-30  3. 30-40\n")
    file_num = randomvalue.intvalue((int(file_level)*10),(int(file_level)*10+10))
    property_flag = input(f"是否添加属性(每个文件内{m_h_num_min}-{m_h_num_max}个)  是：y  默认：否\n")
    white_write_flag = input(f"是否在白名单文件夹写入垃圾代码  是：y  默认：否\n")
    xcodefile_path = ""

    while True:
        xcodefile_path = input("工程文件路径\n")
        xcodefile_path = str(xcodefile_path).strip()
        if os.path.exists(xcodefile_path) == True:
            break
        else:
            print("文件不存在，请重新输入")

    xcodefile_name = os.path.basename(xcodefile_path)
    xcodefile_project_path = f'{xcodefile_path}/{xcodefile_name}.xcodeproj'

    starttime = datetime.datetime.now()

    if white_write_flag == 'y' or white_write_flag == 'Y':
        write_file_list = filemanager.getwhitefile(xcodefile_path,file_while_list)
        for file_item in write_file_list:
            if os.path.splitext(file_item)[-1] == '.h':
                end_num = filemanager.findkeyline(file_item,"@interface")
                filemanager.writestring(file_item,codemodel.property_model(m_h_num_min,m_h_num_max),line_num=(int(end_num)+1))
            if os.path.splitext(file_item)[-1] == '.m':
                end_num = filemanager.findkeyline(file_item,"@implementation")
                for funcnum in range(m_h_num_min,m_h_num_max):
                    func_dic = randomvalue.funccreate(random_func_path,3,None,None)
                    filemanager.writestring(file_item,codemodel.func_model(1,1,1,[],1,func_dic),line_num=(int(end_num)+1))

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


        # 在project添加引用
        subprocess.call(f'ruby {ruby_path} {xcodefile_project_path} {xcodefile_name} {class_name} {xcodefile_path}/{xcodefile_name}/',shell=True)

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
            func_dic = randomvalue.funccreate(random_func_path,3,class_name,1)
            # 函数声明（写进.h中）
            func_head_string = f'{codemodel.constom_func_head_model(func_dic)};'
            filemanager.writestring(h_file,f'{func_head_string}\n',line_num=None)
            # 函数实现（写进.m中）
            if_model_flag = randomvalue.halfprobability()
            while_model_flag = randomvalue.halfprobability()
            switch_model_flag = randomvalue.halfprobability()
            func_write_string = codemodel.func_model(if_model_flag,while_model_flag,switch_model_flag,func_arr,1,func_dic)
            filemanager.writestring(m_file,func_write_string,line_num=None)

    # 调用所有垃圾方法的开关
    print("创建控制开关")
    # 方法实现
    call_all_name = f"{xcodefile_name}AllCall"
    filemanager.create_h_m(f'{xcodefile_path}/{xcodefile_name}',f'{call_all_name}')
    subprocess.call(f'ruby {ruby_path} {xcodefile_project_path} {xcodefile_name} {call_all_name} {xcodefile_path}/{xcodefile_name}/',shell=True)
    filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.m',"- (void)callString{\n\n\n\n\n\n}\n",line_num=None)
    random_func_file = open(random_func_path)
    for line in random_func_file:
        call_string = codemodel.constom_func_call_model(line,1)
        funcdic = eval(line)
        if randomvalue.halfprobability() == 1:
            filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.m',call_string,line_num=7)

    # 方法导入
    total = 4
    random_classfunc_file = open(random_class_name_path,"r")
    for num,value in enumerate(random_classfunc_file):
        total = total+1
        name = str(value).replace('\n','')
        filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.h',f'#import \"{name}.h\"\n' ,line_num=1)
        if property_flag == 'y' or property_flag == 'Y':
            filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{name}.h',codemodel.property_model(m_h_num_min,m_h_num_max),line_num=None)
    random_classfunc_file.close()

    filemanager.writestring(f'{xcodefile_path}/{xcodefile_name}/{call_all_name}.h',"\n- (void)callString;\n",line_num=total)

    print(f'\n垃圾代码的调用在：{call_all_name}.h ...是否开关自行调用')

    endtime = datetime.datetime.now()
    print (f'耗时：{(endtime - starttime).seconds}秒')


if __name__ == '__main__':
    main(sys.argv[1:])