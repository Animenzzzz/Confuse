#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assets 资源指纹差异化模块入口。"""
import argparse
import os
import shutil
import sys

_assets_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_assets_dir)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import profile_loader  # noqa: E402

_argv = sys.argv[1:]
_profile = profile_loader.resolve_profile_name(_argv)
os.environ['CONFUSE_PROFILE'] = _profile

import config  # noqa: E402
import processor  # noqa: E402
import scanner  # noqa: E402
import xcassets  # noqa: E402

config.load_profile(_profile)


def parse_args(argv):
    parser = argparse.ArgumentParser(description='iOS 资源指纹差异化（xcassets / 图片）')
    parser.add_argument('--profile', default=config.active_profile, help='profile 名称')
    parser.add_argument('--project', help='Xcode 工程根目录（含 .xcodeproj 的上一级）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览将处理的文件与操作')
    parser.add_argument('--copy-to', help='输出到新目录（覆盖 profile copy_to）')
    parser.add_argument('--detect-only', action='store_true', help='仅扫描资源，不处理')
    return parser.parse_args(argv)


def resolve_project_path(args):
    if args.project:
        path = args.project.strip()
    else:
        path = input('工程文件路径（含 .xcodeproj 的上一级目录）\n').strip()
    if not os.path.isdir(path):
        raise FileNotFoundError(f'目录不存在: {path}')
    return os.path.abspath(path)


def map_output_path(src_root, out_root, abs_path):
    rel = os.path.relpath(abs_path, src_root)
    return os.path.join(out_root, rel)


def run(args):
    project = resolve_project_path(args)
    config.set_project_root(project)

    if args.copy_to:
        config.copy_to = os.path.abspath(os.path.expanduser(args.copy_to))

    scan_result = scanner.scan_assets(project)
    print(f'\n当前 profile：{config.active_profile}')
    print(f'资源扫描：{scanner.format_scan_log(scan_result)}')

    if args.detect_only:
        if scan_result['counts']['images'] == 0 and scan_result['counts']['xcassets'] == 0:
            return 1
        return 0

    if scan_result['counts']['images'] == 0:
        print('\n未找到可处理的图片资源，已退出。')
        return 1

    dry_run = args.dry_run
    out_root = config.resolve_output_root()
    in_place = os.path.abspath(out_root) == os.path.abspath(project)

    if not in_place and not dry_run:
        if os.path.exists(out_root):
            print(f'输出目录已存在：{out_root}')
        else:
            print(f'复制工程到：{out_root}')
            processor.copy_project_tree(project, out_root)

    processed = 0
    rename_plans = []

    if config.operation_enabled('rename_assets') or config.randomize_imageset_filenames:
        seen = set()
        for item in scan_result['images']:
            imageset_dir = item.get('imageset_dir')
            if not imageset_dir or imageset_dir in seen:
                continue
            seen.add(imageset_dir)
            rename_plans.extend(
                xcassets.plan_imageset_renames(imageset_dir, prefix=config.rename_prefix)
            )

    print(f'\n处理模式：{"预览 (dry-run)" if dry_run else ("原地" if in_place else f"输出到 {out_root}")}')
    print(f'启用操作：{", ".join(config.enabled_operations) or "无"}')
    if config.perturb_enabled and config.operation_enabled('perturb'):
        if not processor.HAS_PILLOW:
            print('提示：未安装 Pillow，perturb 将被跳过（pip install Pillow）')

    for item in scan_result['images']:
        src = item['path']
        dst = src if in_place else map_output_path(project, out_root, src)
        rel = item['rel_path']

        before_hash = processor.file_hash(src) if os.path.isfile(src) and not dry_run else None
        ops = processor.process_image(src, dst, dry_run=dry_run)
        if ops or dry_run:
            suffix = f' → {", ".join(ops)}' if ops else ' → (将处理)'
            print(f'  [{rel}]{suffix}')
            if ops:
                processed += 1
            elif dry_run:
                processed += 1

        if not dry_run and before_hash and os.path.isfile(dst):
            after_hash = processor.file_hash(dst)
            if before_hash != after_hash:
                print(f'    hash: {before_hash} → {after_hash}')

    if rename_plans:
        print(f'\nimageset 重命名：{len(rename_plans)} 项')
        for plan in rename_plans:
            rel_old = os.path.relpath(
                os.path.join(plan['imageset_dir'], plan['old_name']),
                project,
            )
            print(f'  {rel_old} → {plan["new_name"]}')
            if not dry_run:
                xcassets.apply_imageset_rename(plan, dry_run=False)

    print(f'\n完成：{"预览" if dry_run else "已处理"} {processed} 张图片')
    return 0


def main(argv):
    args = parse_args(argv)
    if args.profile:
        config.load_profile(args.profile)
        os.environ['CONFUSE_PROFILE'] = args.profile
    return run(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
