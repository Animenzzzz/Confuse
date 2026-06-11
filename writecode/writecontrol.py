#  Created by Animenzzz on 19/7/12.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.

# 此脚本，README有详细说明

# -*- coding: utf-8 -*-
import argparse
import datetime
import linecache
import os
import subprocess
import sys

import profile_loader

_argv = sys.argv[1:]
_profile = profile_loader.resolve_profile_name(_argv)
os.environ['CONFUSE_PROFILE'] = _profile

import codemodel
import randomvalue
import filemanager
import config

config.load_profile(_profile)
sys.argv = [sys.argv[0]] + _argv

OPTION = """----------------
新建垃圾文件个数：
输入     个数
0       不新建
1       10-20
2       20-30
3       30-40  
----------------
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Objective-C 垃圾代码写入')
    parser.add_argument('--profile', default=config.active_profile, help='profile 名称')
    parser.add_argument('--project', help='Xcode 工程根目录（含 .xcodeproj 的上一级）')
    parser.add_argument(
        '--new-files-level',
        type=int,
        default=-1,
        help='新建文件档位 0-3；-1 为交互',
    )
    parser.add_argument(
        '--new-files',
        type=int,
        default=-1,
        help='新建 .h/.m 文件数量；-1 表示按档位或交互决定',
    )
    parser.add_argument('--inject-white', action='store_true', help='向白名单目录现有 .h/.m 写入')
    parser.add_argument('--add-properties', action='store_true', help='在新建类的 .h 中添加属性')
    return parser.parse_args(argv)


def resolve_project_path(args):
    if args.project:
        path = args.project.strip()
    else:
        path = input('工程文件路径\n').strip()
    if not os.path.isdir(path):
        raise FileNotFoundError(f'目录不存在: {path}')
    config.set_xcodefile_path(path)
    config.set_xcodefile_name(os.path.basename(path))
    config.set_xcodefile_project_path(f'{path}/{config.get_xcodefile_name()}.xcodeproj')
    if config.call_all_class == '':
        config.set_call_all_path(f'{path}/{config.get_xcodefile_name()}')
    else:
        config.set_call_all_path(f'{path}/{config.hx_folder}')


def resolve_new_file_count(args):
    if args.new_files >= 0:
        return args.new_files
    if args.new_files_level >= 0:
        if args.new_files_level == 0:
            return 0
        level = args.new_files_level
        return randomvalue.int_value(level * 10, level * 10 + 10)
    if args.project:
        return 0
    file_level = input(f'{OPTION}').strip()
    if file_level == '0':
        return 0
    level = int(file_level)
    return randomvalue.int_value(level * 10, level * 10 + 10)


def resolve_inject_white(args):
    if args.inject_white:
        return True
    if args.project:
        return False
    flag = input('是否在白名单文件夹写入垃圾代码(是：y  默认：否)\n').strip()
    return flag in ('y', 'Y')


def resolve_add_properties(args):
    if args.add_properties:
        return True
    if args.project:
        return False
    flag = input('是否添加属性(是：y  默认：否)\n').strip()
    return flag in ('y', 'Y')


def writewhite(filepath, whitelist):
    write_file_list = filemanager.get_white_file(filepath, whitelist)
    for file_item in write_file_list:
        if os.path.splitext(file_item)[-1] == '.h':
            end_num = filemanager.find_key_line(file_item, '@interface')
            filemanager.write_string(
                file_item,
                codemodel.property_model(config.m_h_num_min, config.m_h_num_max),
                line_num=(int(end_num) + 1),
            )
        if os.path.splitext(file_item)[-1] == '.m':
            end_num = filemanager.find_key_line(file_item, '@implementation')
            randomint = randomvalue.int_value(config.m_h_num_min, config.m_h_num_max)
            for funcnum in range(randomint):
                func_dic = randomvalue.func_create(config.random_func_path, 3, None, None)
                filemanager.write_string(
                    file_item,
                    codemodel.func_model(1, 1, 1, [], 1, func_dic),
                    line_num=(int(end_num) + 1),
                )


def newlajifile(lajifilenum):

    system_funcfile = open(config.system_func_path, 'r')
    system_func_lengh = len(system_funcfile.readlines())
    system_funcfile.close()

    if os.path.exists(config.random_func_path):
        os.remove(config.random_func_path)

    if os.path.exists(config.random_class_name_path):
        os.remove(config.random_class_name_path)

    print(f'新建的文件个数：{str(lajifilenum)}')
    for index in range(0, lajifilenum):
        new_file_dic = filemanager.create_h_m(
            f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}',
            name=None,
        )
        h_file = new_file_dic['h_path']
        m_file = new_file_dic['m_path']
        class_name = new_file_dic['class_name']

        subprocess.call(
            f'ruby {config.ruby_path} {config.get_xcodefile_project_path()} '
            f'{config.get_xcodefile_name()} {class_name} '
            f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/',
            shell=True,
        )

        classfile = open(config.random_class_name_path, 'a+')
        classfile.writelines(f'{class_name}\n')
        classfile.close()

        func_num = randomvalue.int_value(config.m_h_num_min, config.m_h_num_max)

        for ii in range(1, func_num):
            func_arr = []
            for i in range(1, 3):
                random_row = randomvalue.int_value(1, system_func_lengh)
                random_line = linecache.getline(config.system_func_path, random_row)
                func_arr.append(random_line)
            func_dic = randomvalue.func_create(config.random_func_path, 3, class_name, 1)
            func_head_string = f'{codemodel.constom_func_head_model(func_dic)};'
            filemanager.write_string(h_file, f'{func_head_string}\n', line_num=None)
            if_model_flag = randomvalue.half_probability()
            while_model_flag = randomvalue.half_probability()
            switch_model_flag = randomvalue.half_probability()
            funcwrite_string = codemodel.func_model(
                if_model_flag, while_model_flag, switch_model_flag, func_arr, 1, func_dic,
            )
            filemanager.write_string(m_file, funcwrite_string, line_num=None)


def creatswitch(propertyflag):
    print('\n创建控制开关')
    if config.call_all_class == '':
        call_all_name = f'{config.get_xcodefile_name()}AllCall'
        filemanager.create_h_m(
            f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}',
            f'{call_all_name}',
        )
        subprocess.call(
            f'ruby {config.ruby_path} {config.get_xcodefile_project_path()} '
            f'{config.get_xcodefile_name()} {call_all_name} '
            f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/',
            shell=True,
        )
        filemanager.write_string(
            f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/{call_all_name}.m',
            f'- (void){config.call_func_name}{{\n\n\n\n\n\n}}\n',
            line_num=None,
        )
    else:
        call_all_name = f'{config.call_all_class}'
    random_func_file = open(config.random_func_path)
    for line in random_func_file:
        call_string = codemodel.constom_func_call_model(line, 1)
        if randomvalue.half_probability() == 1:
            if config.call_all_class == '':
                filemanager.write_string(
                    f'{config.get_call_all_path()}/{call_all_name}.m',
                    call_string,
                    line_num=7,
                )
            else:
                line_num = filemanager.find_key_line(
                    f'{config.get_call_all_path()}/{call_all_name}.m',
                    f'{config.call_func_name}',
                )
                filemanager.write_string(
                    f'{config.get_call_all_path()}/{call_all_name}.m',
                    call_string,
                    line_num + 1,
                )

    total = 4
    random_classfunc_file = open(config.random_class_name_path, 'r')
    for num, value in enumerate(random_classfunc_file):
        total = total + 1
        name = str(value).replace('\n', '')
        if config.call_all_class == '':
            line_num = 1
        else:
            line_num = 8
        filemanager.write_string(
            f'{config.get_call_all_path()}/{call_all_name}.h',
            f'#import "{name}.h"\n',
            line_num=line_num,
        )
        if propertyflag:
            filemanager.write_string(
                f'{config.get_xcodefile_path()}/{config.get_xcodefile_name()}/{name}.h',
                codemodel.property_model(config.m_h_num_min, config.m_h_num_max),
                line_num=None,
            )

    random_classfunc_file.close()
    if config.call_all_class == '':
        filemanager.write_string(
            f'{config.get_call_all_path()}/{call_all_name}.h',
            f'\n- (void){config.call_func_name};\n',
            line_num=total,
        )
    print(f'\n垃圾代码的调用在：{call_all_name}.h ...是否开关自行调用')


def run_pipeline(file_num, inject_white, add_properties):
    starttime = datetime.datetime.now()
    if inject_white:
        writewhite(config.get_xcodefile_path(), config.file_while_list)
    if file_num > 0:
        newlajifile(file_num)
        creatswitch(add_properties)
    endtime = datetime.datetime.now()
    print(f'耗时：{(endtime - starttime).seconds}秒')


def main(argv):
    args = parse_args(argv)
    config.load_profile(args.profile)

    print('当前功能模块：【写入垃圾代码】')
    print(f'\n当前 profile：{config.active_profile}')
    print(f'当前文件夹白名单：{config.file_while_list}')

    resolve_project_path(args)

    file_num = resolve_new_file_count(args)
    inject_white = resolve_inject_white(args)
    add_properties = resolve_add_properties(args)
    run_pipeline(file_num, inject_white, add_properties)


if __name__ == '__main__':
    main(_argv)
