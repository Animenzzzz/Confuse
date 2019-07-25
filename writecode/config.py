# -*- coding: utf-8 -*-
import os
import sys

# ----------------需要配置的参数----------------
# 文件夹白名单
# XSDK - 1
# _file_while_list = ["Services","LoginRegister"]
# XSDK - 2
# _file_while_list = ["Services","SKTLoginRegister"]
# XSDK - 3
_file_while_list = ["Services","TFBLoginRegister"]
# XSDK - 4
# _file_while_list = ["Services","ViewController"]
# XSDK - 5
# _file_while_list = ["Services","ViewController"]

# 函数、属性的数量最值
_m_h_num_min = 5
_m_h_num_max = 10

# --------------------------------------------

# 工程路径
_confuse_path = f'{os.path.dirname(sys.path[0])}'
_confuse_resource_path = f'{_confuse_path}/resource'
_system_func_path = f'{_confuse_resource_path}/func_analysised/uikit_class_func.txt'
_random_func_path = f'{_confuse_resource_path}/random_func_create.txt'
_random_class_name_path = f'{_confuse_resource_path}/random_class_name.txt'
_ruby_path = f'{_confuse_path}/writecode/xcodeprojhelp.rb'

# 垃圾代码调用开关
_call_all_path = ""
_call_all_class = "XSDKAllCall" #若设置为空，则默认创建 工程名+AllCall 类作为控制开关
_call_func_name = "callString"

# 全局变量
_xcodefile_path = ""
_xcodefile_name = ""
_xcodefile_project_path = ""

def _set_call_all_path(setvalue):
    global _call_all_path
    _call_all_path = setvalue
    return _call_all_path

def _get_call_all_path():
    global _call_all_path
    return _call_all_path

def _set_xcodefile_path(setvalue):
    global _xcodefile_path
    _xcodefile_path = setvalue
    return _xcodefile_path
    
def _get_xcodefile_path():
    global _xcodefile_path
    return _xcodefile_path

def _set_xcodefile_name(setvalue):
    global _xcodefile_name
    _xcodefile_name = setvalue
    return _xcodefile_name
    
def _get_xcodefile_name():
    global _xcodefile_name
    return _xcodefile_name

def _set_xcodefile_project_path(setvalue):
    global _xcodefile_project_path
    _xcodefile_project_path = setvalue
    return _xcodefile_project_path
    
def _get_xcodefile_project_path():
    global _xcodefile_project_path
    return _xcodefile_project_path