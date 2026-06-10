# -*- coding: utf-8 -*-
import os
import profile_loader

_writecode_dir = os.path.dirname(os.path.abspath(__file__))
confuse_path = os.path.dirname(_writecode_dir)
confuse_resource_path = os.path.join(confuse_path, 'resource')
system_func_path = os.path.join(confuse_resource_path, 'func_analysised/uikit_class_func.txt')
random_func_path = os.path.join(confuse_resource_path, 'random_func_create.txt')
random_class_name_path = os.path.join(confuse_resource_path, 'random_class_name.txt')
ruby_path = os.path.join(confuse_path, 'writecode/xcodeprojhelp.rb')

# 由 profile 覆盖的工程相关配置
file_while_list = []
m_h_num_min = 5
m_h_num_max = 10
call_all_path = ""
call_all_class = ""
call_func_name = "callString"
hx_folder = "HX"
active_profile = "default"

# 运行时由 writecontrol 设置
xcodefile_path = ""
xcodefile_name = ""
xcodefile_project_path = ""


def load_profile(profile_name=None):
    global file_while_list, m_h_num_min, m_h_num_max
    global call_all_class, call_func_name, hx_folder, active_profile

    if profile_name is None:
        profile_name = os.environ.get('CONFUSE_PROFILE', 'default')

    settings = profile_loader.load_writecode_settings(profile_name)
    file_while_list = settings.get('file_while_list', [])
    m_h_num_min = settings.get('m_h_num_min', 5)
    m_h_num_max = settings.get('m_h_num_max', 10)
    call_all_class = settings.get('call_all_class', '')
    call_func_name = settings.get('call_func_name', 'callString')
    hx_folder = settings.get('hx_folder', 'HX')
    active_profile = profile_name
    os.environ['CONFUSE_PROFILE'] = profile_name


load_profile()


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
