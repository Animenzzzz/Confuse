# -*- coding: utf-8 -*-
import os
import re

import codemodel
import config
import randomvalue

TYPE_DECL_RE = re.compile(
    r'^\s*(?:public |private |fileprivate |internal |open |final )*'
    r'(?:class|struct|extension)\s+(\w+)'
)
SKIP_TYPE_RE = re.compile(r'\b(protocol|enum)\s+\w+')


def should_skip_line(line, skip_patterns):
    for pattern in skip_patterns:
        if pattern in line:
            return True
    return False


def is_swift_source(path):
    return os.path.splitext(path)[1] == '.swift'


def path_is_ignored(path):
    parts = path.split(os.sep)
    for ignored in config.ignore_dirs:
        if ignored in parts:
            return True
    if os.path.basename(path) in config.ignore_files:
        return True
    return False


def get_white_swift_files(root_path, whitelist):
    result = set()
    dirlist = []
    for root, dirs, _files in os.walk(root_path):
        for folder_name in whitelist:
            if folder_name in dirs:
                dirlist.append(os.path.join(root, folder_name))
    for folder in dirlist:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in config.ignore_dirs]
            for filename in files:
                full = os.path.join(root, filename)
                if is_swift_source(full) and not path_is_ignored(full):
                    result.add(full)
    return sorted(result)


def find_type_bodies(content, skip_patterns):
    """Return list of (type_name, insert_line_index) for injectable types."""
    lines = content.splitlines(keepends=True)
    results = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if should_skip_line(line, skip_patterns):
            index += 1
            continue
        if SKIP_TYPE_RE.search(line):
            index += 1
            continue
        match = TYPE_DECL_RE.match(line)
        if not match:
            index += 1
            continue
        type_name = match.group(1)
        brace_index = index
        while brace_index < len(lines) and '{' not in lines[brace_index]:
            brace_index += 1
        if brace_index >= len(lines):
            index += 1
            continue
        depth = 0
        body_start = None
        pos = brace_index
        while pos < len(lines):
            for char in lines[pos]:
                if char == '{':
                    depth += 1
                    if depth == 1:
                        body_start = pos
                elif char == '}':
                    depth -= 1
                    if depth == 0 and body_start is not None:
                        insert_at = pos
                        results.append((type_name, insert_at))
                        index = pos + 1
                        break
            else:
                pos += 1
                continue
            break
        else:
            index += 1
    return results, lines


def inject_into_file(filepath, properties=True, methods=True, dry_run=False):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    bodies, lines = find_type_bodies(content, config.skip_line_patterns)
    if not bodies:
        return 0

    injected = 0
    for type_name, line_index in sorted(bodies, key=lambda item: item[1], reverse=True):
        chunk = ''
        if properties:
            chunk += codemodel.property_model(config.member_num_min, config.member_num_max)
        if methods:
            func_count = randomvalue.int_value(config.member_num_min, config.member_num_max)
            for _ in range(func_count):
                func_dic = randomvalue.swift_func_create(type_name)
                chunk += codemodel.func_model(func_dic)
        if not chunk:
            continue
        lines.insert(line_index, chunk)
        injected += 1

    if injected and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return injected


def create_swift_file(out_dir, class_name=None, dry_run=False):
    os.makedirs(out_dir, exist_ok=True)
    if class_name is None:
        class_name = codemodel.new_class_name()
    path = os.path.join(out_dir, f'{class_name}.swift')
    content = codemodel.new_file_content(
        class_name,
        config.member_num_min,
        config.member_num_max,
    )
    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f'生成 Swift 类：{class_name}')
    return {'path': path, 'class_name': class_name, 'content': content}


def write_call_all_calls(call_all_path, class_name, func_name, func_records, class_names, dry_run=False):
    header_path = os.path.join(call_all_path, f'{class_name}.swift')
    if not os.path.isfile(header_path) and not dry_run:
        with open(header_path, 'w', encoding='utf-8') as f:
            f.write(codemodel.call_all_file_content(class_name, func_name))

    if dry_run:
        return

    with open(header_path, encoding='utf-8') as f:
        lines = f.readlines()

    insert_index = None
    for index, line in enumerate(lines):
        if f'func {func_name}()' in line and '{' in line:
            insert_index = index + 1
            break
    if insert_index is None:
        return

    call_lines = []
    for record in func_records:
        call_lines.append(codemodel.func_call_model(record).strip() + '\n')
    for name in class_names:
        call_lines.append(f'{codemodel.TAB}let _ = {name}()\n')

    lines[insert_index:insert_index] = call_lines
    with open(header_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
