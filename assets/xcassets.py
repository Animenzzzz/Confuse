# -*- coding: utf-8 -*-
"""读写 .xcassets 内 Contents.json。"""
import json
import os
import random
import re
import string


def read_contents_json(imageset_dir):
    path = os.path.join(imageset_dir, 'Contents.json')
    if not os.path.isfile(path):
        return None, path
    with open(path, encoding='utf-8') as f:
        return json.load(f), path


def write_contents_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def update_image_filename(contents, old_name, new_name):
    changed = False
    for key in ('images', 'files'):
        items = contents.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            if item.get('filename') == old_name:
                item['filename'] = new_name
                changed = True
    return changed


def random_filename(prefix, ext):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f'{prefix}{suffix}{ext}'


def is_protected_imageset(imageset_dir):
    base = os.path.basename(imageset_dir).lower()
    if base.endswith('.appiconset'):
        return True
    protected = ('appicon', 'launchimage', 'launchscreen')
    return any(p in base for p in protected)


def plan_imageset_renames(imageset_dir, prefix='img_'):
    """为 imageset 内文件规划新文件名（跳过 appiconset）。"""
    if is_protected_imageset(imageset_dir):
        return []

    contents, json_path = read_contents_json(imageset_dir)
    if not contents:
        return []

    plans = []
    for item in contents.get('images', []):
        if not isinstance(item, dict):
            continue
        old_name = item.get('filename')
        if not old_name:
            continue
        ext = os.path.splitext(old_name)[1]
        new_name = random_filename(prefix, ext)
        plans.append({
            'imageset_dir': imageset_dir,
            'contents_path': json_path,
            'old_name': old_name,
            'new_name': new_name,
        })
    return plans


def apply_imageset_rename(plan, dry_run=False):
    imageset_dir = plan['imageset_dir']
    old_path = os.path.join(imageset_dir, plan['old_name'])
    new_path = os.path.join(imageset_dir, plan['new_name'])
    contents, json_path = read_contents_json(imageset_dir)

    if dry_run:
        return True

    if not os.path.isfile(old_path):
        return False

    os.rename(old_path, new_path)
    if contents and update_image_filename(contents, plan['old_name'], plan['new_name']):
        write_contents_json(json_path, contents)
    return True
