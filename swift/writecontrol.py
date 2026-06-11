# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import subprocess
import sys

import profile_loader

_argv = sys.argv[1:]
_profile = profile_loader.resolve_profile_name(_argv)
os.environ['CONFUSE_PROFILE'] = _profile

import codemodel  # noqa: E402
import config  # noqa: E402
import filemanager  # noqa: E402
import randomvalue  # noqa: E402
import rename  # noqa: E402

config.load_profile(_profile)


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Swift 垃圾代码注入与符号重命名')
    parser.add_argument('--profile', default=config.active_profile, help='profile 名称')
    parser.add_argument('--project', help='Xcode 工程根目录（含 .xcodeproj 的上一级）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写入文件')
    parser.add_argument('--inject-white', action='store_true', help='向白名单目录现有 .swift 注入成员')
    parser.add_argument('--new-files', type=int, default=-1, help='新建垃圾 Swift 文件数量；-1 为交互')
    parser.add_argument('--rename', action='store_true', help='执行符号前缀重命名')
    parser.add_argument('--skip-xcode', action='store_true', help='不修改 .xcodeproj')
    return parser.parse_args(argv)


def resolve_project_path(args):
    if args.project:
        path = args.project.strip()
    else:
        path = input('工程文件路径（含 .xcodeproj 的上一级目录）\n').strip()
    if not os.path.isdir(path):
        raise FileNotFoundError(f'目录不存在: {path}')
    config.set_xcodefile_path(path)
    config.set_xcodefile_name(os.path.basename(path))
    xcodeproj = f'{path}/{config.get_xcodefile_name()}.xcodeproj'
    if os.path.isdir(xcodeproj):
        config.set_xcodefile_project_path(xcodeproj)
    if config.call_all_class:
        config.set_call_all_path(f'{path}/{config.hx_folder}')
    else:
        config.set_call_all_path(config.output_root())


def register_swift_in_xcode(class_name, swift_dir, dry_run, skip_xcode):
    if dry_run or skip_xcode:
        return
    if not config.get_xcodefile_project_path():
        print('未找到 .xcodeproj，跳过工程注册')
        return
    subprocess.call(
        f'ruby {config.ruby_path} '
        f'{config.get_xcodefile_project_path()} '
        f'{config.get_xcodefile_name()} '
        f'{class_name} '
        f'{swift_dir}/',
        shell=True,
    )


def inject_whitelist(dry_run):
    files = filemanager.get_white_swift_files(config.get_xcodefile_path(), config.file_while_list)
    total = 0
    for path in files:
        count = filemanager.inject_into_file(
            path,
            properties=config.inject_properties,
            methods=config.inject_methods,
            dry_run=dry_run,
        )
        total += count
        if count:
            print(f'注入 {count} 处：{path}')
    print(f'白名单注入完成，共 {total} 处{"（dry-run）" if dry_run else ""}')


def create_new_files(count, dry_run, skip_xcode):
    out_dir = config.output_root()
    if os.path.exists(config.random_class_name_path):
        os.remove(config.random_class_name_path)
    if os.path.exists(config.random_func_path):
        os.remove(config.random_func_path)

    class_names = []
    func_records = []
    print(f'新建 Swift 文件：{count} 个')
    for _ in range(count):
        info = filemanager.create_swift_file(out_dir, dry_run=dry_run)
        class_name = info['class_name']
        class_names.append(class_name)
        register_swift_in_xcode(class_name, out_dir, dry_run, skip_xcode)
        if not dry_run:
            with open(config.random_class_name_path, 'a', encoding='utf-8') as f:
                f.write(f'{class_name}\n')
        func_count = randomvalue.int_value(config.member_num_min, config.member_num_max)
        for _ in range(func_count):
            func_dic = randomvalue.swift_func_create(class_name, config.random_func_path if not dry_run else None)
            func_records.append(func_dic)

    create_call_switch(class_names, func_records, dry_run)


def create_call_switch(class_names, func_records, dry_run):
    if config.call_all_class:
        call_all_name = config.call_all_class
    else:
        call_all_name = f'{config.get_xcodefile_name()}SwiftAllCall'
        call_path = os.path.join(config.get_call_all_path(), f'{call_all_name}.swift')
        if not dry_run:
            os.makedirs(config.get_call_all_path(), exist_ok=True)
            with open(call_path, 'w', encoding='utf-8') as f:
                f.write(codemodel.call_all_file_content(call_all_name, config.call_func_name))

    filemanager.write_call_all_calls(
        config.get_call_all_path(),
        call_all_name,
        config.call_func_name,
        func_records,
        class_names,
        dry_run=dry_run,
    )
    print(f'调用入口：{call_all_name}.{config.call_func_name}()')


def interactive_new_file_count():
    option = """
----------------
新建垃圾 Swift 文件个数：
输入     个数
0       不新建
1       5-15
2       15-25
3       25-35
----------------
"""
    level = input(option).strip()
    if level == '0':
        return 0
    base = int(level) * 10 if level.isdigit() else config.new_file_count_min
    return randomvalue.int_value(
        max(base, config.new_file_count_min),
        max(base + 10, config.new_file_count_max),
    )


def main(argv):
    args = parse_args(argv)
    config.load_profile(args.profile)

    print('当前功能模块：【Swift 垃圾代码 / 重命名】')
    print(f'当前 profile：{config.active_profile}')
    print(f'白名单目录：{config.file_while_list}')

    resolve_project_path(args)

    inject_white = args.inject_white
    new_count = args.new_files
    do_rename = args.rename or config.rename_enabled

    if not inject_white and new_count < 0 and not do_rename:
        flag = input('是否在白名单目录注入成员？(y/N)\n').strip().lower()
        inject_white = flag == 'y'
        new_count = interactive_new_file_count()
        rename_flag = input('是否执行符号前缀重命名？(y/N)\n').strip().lower()
        do_rename = rename_flag == 'y'

    start = datetime.datetime.now()

    if inject_white:
        inject_whitelist(args.dry_run)

    if new_count < 0:
        new_count = 0
    if new_count > 0:
        create_new_files(new_count, args.dry_run, args.skip_xcode)

    if do_rename:
        rename.run_rename(
            config.get_xcodefile_path(),
            config.file_while_list,
            dry_run=args.dry_run,
        )

    elapsed = (datetime.datetime.now() - start).seconds
    print(f'耗时：{elapsed} 秒')


if __name__ == '__main__':
    main(_argv)
