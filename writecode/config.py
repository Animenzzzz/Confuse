# -*- coding: utf-8 -*-
import os
import sys

# ----------------需要配置的参数----------------
# 文件夹白名单
# XSDK - 1
# file_while_list = ["Services","LoginRegister"]
# XSDK - 2
# file_while_list = ["Services","SKTLoginRegister"]
# XSDK - 3
file_while_list = ["Services","TFBLoginRegister"]
# XSDK - 4
# file_while_list = ["Services","ViewController"]
# XSDK - 5
# file_while_list = ["Services","ViewController"]

# 函数、属性的数量最值
m_h_num_min = 5
m_h_num_max = 10

# --------------------------------------------

# 工程路径
confuse_path = f'{os.path.dirname(sys.path[0])}'
confuse_resource_path = f'{confuse_path}/resource'
system_func_path = f'{confuse_resource_path}/func_analysised/uikit_class_func.txt'
random_func_path = f'{confuse_resource_path}/random_func_create.txt'
random_class_name_path = f'{confuse_resource_path}/random_class_name.txt'
ruby_path = f'{confuse_path}/writecode/xcodeprojhelp.rb'

# 垃圾代码调用开关
call_all_path = ""
call_all_class = "XSDKAllCall" #若设置为空，则默认创建 工程名+AllCall 类作为控制开关
call_func_name = "callString"

# 全局变量
xcodefile_path = ""
xcodefile_name = ""
xcodefile_project_path = ""

def set_call_all_path(setvalue):
    global call_all_path
    call_all_path = setvalue
    return call_all_path

def get_call_all_path():
    global call_all_path
    return call_all_path

def set_xcodefile_path(setvalue):
    global xcodefile_path
    xcodefile_path = setvalue
    return xcodefile_path
    
def get_xcodefile_path():
    global xcodefile_path
    return xcodefile_path

def set_xcodefile_name(setvalue):
    global xcodefile_name
    xcodefile_name = setvalue
    return xcodefile_name
    
def get_xcodefile_name():
    global xcodefile_name
    return xcodefile_name

def set_xcodefile_project_path(setvalue):
    global xcodefile_project_path
    xcodefile_project_path = setvalue
    return xcodefile_project_path
    
def get_xcodefile_project_path():
    global xcodefile_project_path
    return xcodefile_project_path