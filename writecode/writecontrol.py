# -*- coding: utf-8 -*-
import codemodel
import os
import linecache
import randomvalue
import filemanager
import subprocess
import sys
import datetime
import config

OPTION = """----------------
新建垃圾文件个数：
输入     个数
0       不新建
1       10-20
2       20-30
3       30-40  
----------------
"""

def main(argv):
    print(f'\n当前文件夹白名单：{config.file_while_list}')
    file_level = input(f'{OPTION}')
    file_num = randomvalue.int_value((int(file_level)*10),(int(file_level)*10+10))
    property_flag = input(f"是否添加属性(是：y  默认：否)\n")
    white_write_flag = input(f"是否在白名单文件夹写入垃圾代码(是：y  默认：否)\n")

    while True:
        inpustring = input("工程文件路径\n")
        config.set_xcodefile_path(str(inpustring).strip())
        if os.path.exists(config.get_xcodefile_path()) == True:
            break
        else:
            print("文件不存在，请重新输入")

    config.set_xcodefile_name(os.path.basename(config.get_xcodefile_path()))
    config.set_xcodefile_project_path(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}.xcodeproj')
    if config.call_all_class == "":
        config.set_call_all_path(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}')
    else:
        config.set_call_all_path(f'{config.get_xcodefile_path()}/HX/')

    starttime = datetime.datetime.now()

    if white_write_flag == 'y' or white_write_flag == 'Y':
        writewhite(config.get_xcodefile_path(),config.file_while_list)

    if file_level != '0':
        newlajifile(file_num)
        creatswitch(property_flag)

    endtime = datetime.datetime.now()
    print (f'耗时：{(endtime - starttime).seconds}秒')

def writewhite(filepath,whitelist):
    write_file_list = filemanager.get_white_file(filepath,whitelist)
    for file_item in write_file_list:
        if os.path.splitext(file_item)[-1] == '.h':
            end_num = filemanager.find_key_line(file_item,"@interface")
            filemanager.write_string(file_item,codemodel.property_model(config.m_h_num_min,config.m_h_num_max),line_num=(int(end_num)+1))
        if os.path.splitext(file_item)[-1] == '.m':
            end_num = filemanager.find_key_line(file_item,"@implementation")
            randomint = randomvalue.int_value(config.m_h_num_min,config.m_h_num_max)
            for funcnum in range(randomint):
                func_dic = randomvalue.func_create(config.random_func_path,3,None,None)
                filemanager.write_string(file_item,codemodel.func_model(1,1,1,[],1,func_dic),line_num=(int(end_num)+1))

def newlajifile(lajifilenum):
  
    system_funcfile = open(config.system_func_path,'r')
    system_func_lengh = len(system_funcfile.readlines())
    system_funcfile.close()

    if os.path.exists(config.random_func_path):
        os.remove(config.random_func_path)

    if os.path.exists(config.random_class_name_path):
        os.remove(config.random_class_name_path)

    print(f'新建的文件个数：{str(lajifilenum)}')
    for index in range(0,lajifilenum):
        new_file_dic = filemanager.create_h_m(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}',name=None)
        h_file = new_file_dic["h_path"]
        m_file = new_file_dic["m_path"]
        class_name = new_file_dic["class_name"]


        # 在project添加引用
        subprocess.call(f'ruby {config.ruby_path} {config.get_xcodefile_project_path()} {config.get_xcodefile_name()} {class_name} {config.get_xcodefile_path()}/{config.get_xcodefile_name()}/',shell=True)

        classfile = open(config.random_class_name_path,'a+')
        classfile.writelines(f'{class_name}\n')
        classfile.close()

        # 函数个数
        func_num = randomvalue.int_value(config.m_h_num_min,config.m_h_num_max)

        for ii in range(1,func_num):
            func_arr = []
            # 获取系统方法的字符串
            for i in range(1,3):
                random_row = randomvalue.int_value(1,system_func_lengh)
                random_line = linecache.getline(config.system_func_path, random_row)
                func_arr.append(random_line)
            # 创建随机函数并且写入txt文件，函数信息，包括返回类型、参数等
            func_dic = randomvalue.func_create(config.random_func_path,3,class_name,1)
            # 函数声明（写进.h中）
            func_head_string = f'{codemodel.constom_func_head_model(func_dic)};'
            filemanager.write_string(h_file,f'{func_head_string}\n',line_num=None)
            # 函数实现（写进.m中）
            if_model_flag = randomvalue.half_probability()
            while_model_flag = randomvalue.half_probability()
            switch_model_flag = randomvalue.half_probability()
            funcwrite_string = codemodel.func_model(if_model_flag,while_model_flag,switch_model_flag,func_arr,1,func_dic)
            filemanager.write_string(m_file,funcwrite_string,line_num=None)

def creatswitch(propertyflag):
    # 调用所有垃圾方法的开关
    print("\n创建控制开关")
    # 方法实现
    if config.call_all_class == "":
        call_all_name = f"{config.get_xcodefile_name()}AllCall"
        filemanager.create_h_m(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}',f'{call_all_name}')
        subprocess.call(f'ruby {config.ruby_path} {config.get_xcodefile_project_path()} {config.get_xcodefile_name()} {call_all_name} {config.get_xcodefile_path()}/{config.get_xcodefile_name()}/',shell=True)
        filemanager.write_string(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/{call_all_name}.m',f"- (void){config.call_func_name}{{\n\n\n\n\n\n}}\n",line_num=None)
    else:
        call_all_name = f"{config.call_all_class}"
    random_func_file = open(config.random_func_path)
    for line in random_func_file:
        call_string = codemodel.constom_func_call_model(line,1)
        funcdic = eval(line)
        if randomvalue.half_probability() == 1:
            if config.call_all_class == "":
                filemanager.write_string(f'{config.get_call_all_path()}/{call_all_name}.m',call_string,line_num=7)
            else:
                line_num = filemanager.find_key_line(f'{config.get_call_all_path()}/{call_all_name}.m',f'{config.call_func_name}')
                filemanager.write_string(f'{config.get_call_all_path()}/{call_all_name}.m',call_string,line_num+1)

    # 方法导入
    total = 4
    random_classfunc_file = open(config.random_class_name_path,"r")
    for num,value in enumerate(random_classfunc_file):
        total = total+1
        name = str(value).replace('\n','')
        line_num = 0
        if config.call_all_class == "":
            line_num = 1
        else:
            line_num = 8
        filemanager.write_string(f'{config.get_call_all_path()}/{call_all_name}.h',f'#import \"{name}.h\"\n' ,line_num=line_num)
        if propertyflag == 'y' or propertyflag == 'Y':
            filemanager.write_string(f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/{name}.h',codemodel.property_model(config.m_h_num_min,config.m_h_num_max),line_num=None)

    random_classfunc_file.close()
    if config.call_all_class == "":
        filemanager.write_string(f'{config.get_call_all_path()}/{call_all_name}.h',f"\n- (void){config.call_func_name};\n",line_num=total)
    print(f'\n垃圾代码的调用在：{call_all_name}.h ...是否开关自行调用')

if __name__ == '__main__':
    main(sys.argv[1:])