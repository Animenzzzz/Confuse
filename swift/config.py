# -*- coding: utf-8 -*-
import os

import profile_loader

_swift_dir = os.path.dirname(os.path.abspath(__file__))
confuse_path = os.path.dirname(_swift_dir)
confuse_resource_path = os.path.join(confuse_path, 'resource')
random_class_name_path = os.path.join(confuse_resource_path, 'random_swift_class_name.txt')
random_func_path = os.path.join(confuse_resource_path, 'random_swift_func_create.txt')
rename_map_path = os.path.join(confuse_resource_path, 'swift_rename_map.json')
ruby_path = os.path.join(_swift_dir, 'xcodeprojhelp_swift.rb')

file_while_list = []
member_num_min = 3
member_num_max = 8
new_file_count_min = 5
new_file_count_max = 15
call_all_class = ''
call_func_name = 'invokeObfuscation'
hx_folder = 'HX'
output_subdir = ''
inject_properties = True
inject_methods = True
rename_enabled = False
rename_prefix = 'Obf'
rename_types = True
rename_functions = True
rename_properties = False
skip_line_patterns = []
ignore_dirs = []
ignore_files = []
active_profile = 'default'

xcodefile_path = ''
xcodefile_name = ''
xcodefile_project_path = ''
call_all_path = ''


def load_profile(profile_name=None):
    global file_while_list, member_num_min, member_num_max
    global new_file_count_min, new_file_count_max
    global call_all_class, call_func_name, hx_folder, output_subdir
    global inject_properties, inject_methods
    global rename_enabled, rename_prefix, rename_types, rename_functions, rename_properties
    global skip_line_patterns, ignore_dirs, ignore_files, active_profile

    if profile_name is None:
        profile_name = os.environ.get('CONFUSE_PROFILE', 'default')

    settings = profile_loader.load_swift_settings(profile_name)
    file_while_list = settings.get('file_while_list', [])
    member_num_min = settings.get('member_num_min', 3)
    member_num_max = settings.get('member_num_max', 8)
    new_file_count_min = settings.get('new_file_count_min', 5)
    new_file_count_max = settings.get('new_file_count_max', 15)
    call_all_class = settings.get('call_all_class', '')
    call_func_name = settings.get('call_func_name', 'invokeObfuscation')
    hx_folder = settings.get('hx_folder', 'HX')
    output_subdir = settings.get('output_subdir', '')
    inject_properties = settings.get('inject_properties', True)
    inject_methods = settings.get('inject_methods', True)
    rename_enabled = settings.get('rename_enabled', False)
    rename_prefix = settings.get('rename_prefix', 'Obf')
    rename_types = settings.get('rename_types', True)
    rename_functions = settings.get('rename_functions', True)
    rename_properties = settings.get('rename_properties', False)
    skip_line_patterns = settings.get('skip_line_patterns', [])
    ignore_dirs = settings.get('ignore_dirs', [])
    ignore_files = settings.get('ignore_files', [])
    active_profile = profile_name
    os.environ['CONFUSE_PROFILE'] = profile_name


load_profile()


def set_xcodefile_path(value):
    global xcodefile_path
    xcodefile_path = value


def get_xcodefile_path():
    return xcodefile_path


def set_xcodefile_name(value):
    global xcodefile_name
    xcodefile_name = value


def get_xcodefile_name():
    return xcodefile_name


def set_xcodefile_project_path(value):
    global xcodefile_project_path
    xcodefile_project_path = value


def get_xcodefile_project_path():
    return xcodefile_project_path


def set_call_all_path(value):
    global call_all_path
    call_all_path = value


def get_call_all_path():
    return call_all_path


def output_root():
    base = get_xcodefile_path()
    if output_subdir:
        return os.path.join(base, output_subdir)
    return os.path.join(base, get_xcodefile_name())
