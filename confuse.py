#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confuse 统一入口：扫描 Xcode 工程，自动选择 OC / Swift 混淆模块。

仍可直接使用各子模块入口（向后兼容）：
  python3 writecode/writecontrol.py
  python3 swift/writecontrol.py
  sh rename/func.sh
"""
import argparse
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

sys.path.insert(0, os.path.join(REPO_ROOT, 'writecode'))
import profile_loader  # noqa: E402

from auto_config import load_auto_settings  # noqa: E402
from project_detect import format_detection_log, resolve_modules, scan_project  # noqa: E402

NEW_FILES_OPTION = """
----------------
新建垃圾文件个数（OC / Swift 共用）：
输入     参考个数
0       不新建
1       约 10-20
2       约 20-30
3       约 30-40
----------------
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Confuse 统一入口：自动检测 OC / Swift 并运行对应模块',
    )
    parser.add_argument('--profile', help='profile 名称（默认 default 或 CONFUSE_PROFILE）')
    parser.add_argument(
        '--project',
        help='Xcode 工程根目录（含 .xcodeproj 的上一级）；省略则交互输入',
    )
    parser.add_argument(
        '--detect-only',
        action='store_true',
        help='仅扫描并输出检测结果，不执行混淆',
    )
    parser.add_argument('--dry-run', action='store_true', help='Swift 模块仅预览（OC 模块不支持）')
    parser.add_argument('--inject-white', action='store_true', help='向白名单目录注入/写入垃圾代码')
    parser.add_argument(
        '--new-files',
        type=int,
        default=-1,
        help='新建垃圾源文件数量；-1 为交互或按档位',
    )
    parser.add_argument(
        '--new-files-level',
        type=int,
        default=-1,
        help='新建文件档位 0-3（OC / Swift 交互档位）；--new-files 优先',
    )
    parser.add_argument('--add-properties', action='store_true', help='OC：在新建类 .h 中添加属性')
    parser.add_argument('--rename', action='store_true', help='Swift：执行符号前缀重命名')
    parser.add_argument('--skip-xcode', action='store_true', help='Swift：不修改 .xcodeproj')
    return parser.parse_args(argv)


def resolve_project_path(args):
    if args.project:
        return os.path.abspath(os.path.expanduser(args.project.strip()))
    while True:
        path = input('工程文件路径（含 .xcodeproj 的上一级目录）\n').strip()
        if os.path.isdir(path):
            return os.path.abspath(path)
        print('目录不存在，请重新输入')


def interactive_new_file_count():
    level = input(NEW_FILES_OPTION).strip()
    if level == '0':
        return 0
    if level.isdigit():
        base = int(level) * 10
        return base if base > 0 else 10
    return 10


def interactive_flags(args, modules):
    inject_white = args.inject_white
    new_files = args.new_files
    do_rename = args.rename
    add_properties = args.add_properties

    need_prompt = (
        not inject_white
        and new_files < 0
        and not do_rename
        and not add_properties
    )
    if need_prompt:
        flag = input('是否在白名单目录注入/写入垃圾代码？(y/N)\n').strip().lower()
        inject_white = flag == 'y'
        new_files = interactive_new_file_count()
        if modules.get('swift'):
            rename_flag = input('是否执行 Swift 符号前缀重命名？(y/N)\n').strip().lower()
            do_rename = rename_flag == 'y'
        if modules.get('oc') and new_files > 0:
            prop_flag = input('OC 新建类是否在 .h 中添加属性？(y/N)\n').strip().lower()
            add_properties = prop_flag == 'y'

    if new_files < 0:
        if args.new_files_level >= 0:
            if args.new_files_level == 0:
                new_files = 0
            else:
                new_files = args.new_files_level * 10
        else:
            new_files = 0

    return inject_white, new_files, do_rename, add_properties


def build_oc_argv(profile, project, inject_white, new_files, new_files_level, add_properties):
    argv = [
        sys.executable,
        os.path.join(REPO_ROOT, 'writecode', 'writecontrol.py'),
        '--profile',
        profile,
        '--project',
        project,
    ]
    if inject_white:
        argv.append('--inject-white')
    if add_properties:
        argv.append('--add-properties')
    if new_files >= 0:
        argv.extend(['--new-files', str(new_files)])
    elif new_files_level >= 0:
        argv.extend(['--new-files-level', str(new_files_level)])
    return argv


def build_swift_argv(
    profile,
    project,
    inject_white,
    new_files,
    do_rename,
    dry_run,
    skip_xcode,
):
    argv = [
        sys.executable,
        os.path.join(REPO_ROOT, 'swift', 'writecontrol.py'),
        '--profile',
        profile,
        '--project',
        project,
    ]
    if inject_white:
        argv.append('--inject-white')
    if new_files >= 0:
        argv.extend(['--new-files', str(new_files)])
    if do_rename:
        argv.append('--rename')
    if dry_run:
        argv.append('--dry-run')
    if skip_xcode:
        argv.append('--skip-xcode')
    return argv


def run_subprocess(argv, label):
    print(f'\n>>> 启动 {label}')
    print(f'>>> {" ".join(argv[2:])}')
    result = subprocess.run(argv, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f'>>> {label} 退出码：{result.returncode}', file=sys.stderr)
        return result.returncode
    return 0


def main(argv):
    args = parse_args(argv)
    profile = args.profile or profile_loader.resolve_profile_name([])
    os.environ['CONFUSE_PROFILE'] = profile

    auto_settings = load_auto_settings(profile)
    project = resolve_project_path(args)
    detection = scan_project(project, ignore_dirs=auto_settings.get('ignore_dirs'))
    modules = resolve_modules(detection, auto_settings.get('enabled_modules'))

    print(f'\n当前 profile：{profile}')
    print(format_detection_log(detection, modules))

    if args.detect_only:
        return 0

    if not modules['oc'] and not modules['swift']:
        print('\n未检测到可处理的 OC（.m）或 Swift 源文件，已退出。')
        print('提示：纯头文件工程（仅有 .h 无 .m）不会触发 OC 模块。')
        return 1

    inject_white, new_files, do_rename, add_properties = interactive_flags(args, modules)

    exit_code = 0
    if modules['oc']:
        oc_argv = build_oc_argv(
            profile,
            project,
            inject_white,
            new_files,
            args.new_files_level,
            add_properties,
        )
        code = run_subprocess(oc_argv, 'OC writecode')
        exit_code = max(exit_code, code)

    if modules['swift']:
        swift_argv = build_swift_argv(
            profile,
            project,
            inject_white,
            new_files,
            do_rename,
            args.dry_run,
            args.skip_xcode,
        )
        code = run_subprocess(swift_argv, 'Swift writecontrol')
        exit_code = max(exit_code, code)

    if modules['oc'] and do_rename:
        print(
            '\n提示：OC 函数/工程前缀重命名请单独运行 rename/func.sh 或 rename/projectfile.sh。'
        )

    return exit_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
