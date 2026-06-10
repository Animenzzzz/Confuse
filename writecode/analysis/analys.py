# -*- coding: utf-8 -*-
import analysisstring
import os

_confuse_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
work_path = os.path.join(_confuse_root, 'resource')

file_path1 = os.path.join(work_path, 'func_orign/uikit_class_func.txt')
file_json_path1 = os.path.join(work_path, 'func_analysised/uikit_class_func.txt')

file_path2 = os.path.join(work_path, 'func_orign/uikit_class_instancetype_func.txt')
file_json_path2 = os.path.join(work_path, 'func_analysised/uikit_class_instancetype_func.txt')

file_path3 = os.path.join(work_path, 'func_orign/uikit_member_func.txt')
file_json_path3 = os.path.join(work_path, 'func_analysised/uikit_member_func.txt')

file_path4 = os.path.join(work_path, 'func_orign/uikit_member_instancetype_func.txt')
file_json_path4 = os.path.join(work_path, 'func_analysised/uikit_member_instancetype_func.txt')

if os.path.exists(file_json_path1):
    os.remove(file_json_path1)

if os.path.exists(file_json_path2):
    os.remove(file_json_path2)

if os.path.exists(file_json_path3):
    os.remove(file_json_path3)

if os.path.exists(file_json_path4):
    os.remove(file_json_path4)

for line in open(file_path1):
    analysisstring.func(f'{line}', file_json_path1)

for line in open(file_path2):
    analysisstring.func(f'{line}', file_json_path2)

for line in open(file_path3):
    analysisstring.func(f'{line}', file_json_path3)

for line in open(file_path4):
    analysisstring.func(f'{line}', file_json_path4)
