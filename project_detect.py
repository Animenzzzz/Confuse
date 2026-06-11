# -*- coding: utf-8 -*-
"""扫描 Xcode 工程目录，统计 OC / Swift 源文件并决定运行哪些模块。"""
import os

DEFAULT_IGNORE_DIRS = frozenset({
    'Pods',
    'Carthage',
    'Build',
    '.git',
    'DerivedData',
    '.build',
    '3rd',
    'Index',
    '.svn',
    'node_modules',
})


def normalize_project_root(path):
    path = os.path.abspath(os.path.expanduser(path.strip()))
    if not os.path.isdir(path):
        raise FileNotFoundError(f'目录不存在: {path}')
    return path


def scan_project(project_root, ignore_dirs=None):
    """递归统计 .m / .h / .swift，跳过 ignore_dirs 中的目录名。"""
    root = normalize_project_root(project_root)
    ignored = set(DEFAULT_IGNORE_DIRS)
    if ignore_dirs:
        ignored.update(ignore_dirs)

    counts = {'m': 0, 'h': 0, 'swift': 0}
    for dir_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ignored]
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.m':
                counts['m'] += 1
            elif ext == '.h':
                counts['h'] += 1
            elif ext == '.swift':
                counts['swift'] += 1

    has_oc = counts['m'] > 0
    has_swift = counts['swift'] > 0
    return {
        'project_root': root,
        'counts': counts,
        'has_oc': has_oc,
        'has_swift': has_swift,
        'ignore_dirs': sorted(ignored),
    }


def resolve_modules(detection, enabled_modules=None):
    """
    根据扫描结果或 profile 覆盖项决定运行模块。
    enabled_modules: None 表示自动；否则为 ['oc', 'swift'] 的子集。
    """
    if enabled_modules is not None:
        allowed = {m.lower() for m in enabled_modules}
        return {
            'oc': 'oc' in allowed,
            'swift': 'swift' in allowed,
        }
    return {
        'oc': detection['has_oc'],
        'swift': detection['has_swift'],
    }


def format_detection_log(detection, modules):
    c = detection['counts']
    parts = []
    if c['m'] or c['h']:
        parts.append(f'Objective-C ({c["m"]} .m, {c["h"]} .h)')
    if c['swift']:
        parts.append(f'Swift ({c["swift"]} files)')
    if not parts:
        parts.append('未检测到 .m / .swift 源文件')

    run_parts = []
    if modules['oc']:
        run_parts.append('OC writecode')
    if modules['swift']:
        run_parts.append('Swift writecontrol')
    run_text = '、'.join(run_parts) if run_parts else '无（请检查工程路径或 profile enabled_modules）'
    return f'Detected: {", ".join(parts)} → running {run_text}'
