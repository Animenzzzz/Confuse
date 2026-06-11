# -*- coding: utf-8 -*-
import json
import os
import re

import config
import randomvalue

RESERVED = {
    'self', 'super', 'init', 'deinit', 'Self', 'true', 'false', 'nil',
    'viewDidLoad', 'viewWillAppear', 'viewDidAppear', 'viewWillDisappear',
    'viewDidDisappear', 'didReceiveMemoryWarning', 'prepare', 'encode',
    'decode', 'copy', 'description', 'hash', 'isEqual', 'awakeFromNib',
    'layoutSubviews', 'draw', 'main', 'application', 'scene',
}

TYPE_RE = re.compile(
    r'^\s*(?:public |private |fileprivate |internal |open |final )*'
    r'(class|struct|enum)\s+(\w+)'
)
FUNC_RE = re.compile(
    r'^\s*(?:@\w+\s+)*(?:public |private |fileprivate |internal |open |override |static |class )*'
    r'func\s+(\w+)\s*\('
)
VAR_RE = re.compile(
    r'^\s*(?:@\w+\s+)*(?:public |private |fileprivate |internal |open |override |static |lazy )*'
    r'(?:var|let)\s+(\w+)'
)


def should_skip_rename_line(line):
    for pattern in config.skip_line_patterns:
        if pattern in line:
            return True
    if line.strip().startswith('//'):
        return True
    return False


def collect_symbols(filepath):
    types = set()
    functions = set()
    properties = set()
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            if should_skip_rename_line(line):
                continue
            type_match = TYPE_RE.match(line)
            if type_match:
                types.add(type_match.group(2))
            func_match = FUNC_RE.match(line)
            if func_match:
                functions.add(func_match.group(1))
            var_match = VAR_RE.match(line)
            if var_match:
                properties.add(var_match.group(1))
    return types, functions, properties


def build_rename_map(swift_files):
    mapping = {'types': {}, 'functions': {}, 'properties': {}}
    all_types = set()
    all_functions = set()
    all_properties = set()

    for path in swift_files:
        types, functions, properties = collect_symbols(path)
        all_types.update(types)
        all_functions.update(functions)
        all_properties.update(properties)

    prefix = config.rename_prefix

    def new_name(old):
        if old in RESERVED or old.startswith(prefix):
            return old
        return f'{prefix}{old[0].upper()}{old[1:]}' if old else old

    if config.rename_types:
        for name in sorted(all_types):
            if name not in RESERVED:
                mapping['types'][name] = new_name(name)

    if config.rename_functions:
        for name in sorted(all_functions):
            if name not in RESERVED and not name.startswith('init'):
                mapping['functions'][name] = new_name(name)

    if config.rename_properties:
        for name in sorted(all_properties):
            if name not in RESERVED:
                mapping['properties'][name] = new_name(name)

    return mapping


def apply_rename_to_file(filepath, mapping, dry_run=False):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    updated = content
    combined = {}
    combined.update(mapping.get('types', {}))
    combined.update(mapping.get('functions', {}))
    combined.update(mapping.get('properties', {}))

    for old, new in sorted(combined.items(), key=lambda item: -len(item[0])):
        if old == new:
            continue
        updated = re.sub(r'\b' + re.escape(old) + r'\b', new, updated)

    if updated != content and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
    return updated != content


def run_rename(root_path, whitelist, dry_run=False):
    from filemanager import get_white_swift_files

    files = get_white_swift_files(root_path, whitelist)
    if not files:
        print('未找到可重命名的 Swift 文件')
        return {}

    mapping = build_rename_map(files)
    changed = 0
    for path in files:
        if apply_rename_to_file(path, mapping, dry_run=dry_run):
            changed += 1

    if not dry_run:
        with open(config.rename_map_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f'重命名：{changed} 个文件{"（dry-run，未写入）" if dry_run else ""}')
    print(f'映射表：{config.rename_map_path}')
    return mapping
