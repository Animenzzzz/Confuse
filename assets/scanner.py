# -*- coding: utf-8 -*-
"""扫描工程内的 .xcassets 与独立图片资源。"""
import os

from project_detect import DEFAULT_IGNORE_DIRS

import config

IMAGE_EXTENSIONS = config.IMAGE_EXTENSIONS


def _should_ignore_dir(dirname, ignored):
    if dirname in ignored:
        return True
    if dirname.endswith('.framework'):
        return True
    return False


def _path_matches_skip(path, skip_patterns):
    norm = path.replace(os.sep, '/')
    for pattern in skip_patterns:
        if pattern in norm:
            return True
    return False


def _in_whitelist(rel_parts):
    if config.scan_whole_project or not config.file_while_list:
        return True
    for part in rel_parts:
        if part in config.file_while_list:
            return True
    return False


def _collect_ignored():
    ignored = set(DEFAULT_IGNORE_DIRS)
    ignored.update(config.ignore_dirs)
    return ignored


def scan_assets(project_root):
    """
    返回扫描结果字典：
      xcassets: [.xcassets 目录绝对路径, ...]
      images: [{path, rel_path, in_xcassets, imageset_dir?}, ...]
      counts: {xcassets, images, imagesets}
    """
    root = os.path.abspath(os.path.expanduser(project_root))
    ignored = _collect_ignored()
    skip_patterns = config.skip_patterns

    xcassets_dirs = []
    images = []
    imageset_count = 0

    for dir_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not _should_ignore_dir(d, ignored)]

        rel_dir = os.path.relpath(dir_root, root)
        rel_parts = [] if rel_dir == '.' else rel_dir.split(os.sep)

        for dirname in list(dirs):
            if dirname.endswith('.xcassets'):
                xc_path = os.path.join(dir_root, dirname)
                if _path_matches_skip(xc_path, skip_patterns):
                    continue
                if _in_whitelist(rel_parts + [dirname]):
                    xcassets_dirs.append(xc_path)

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue

            abs_path = os.path.join(dir_root, filename)
            if _path_matches_skip(abs_path, skip_patterns):
                continue

            in_xcassets = '.xcassets' in abs_path
            if not in_xcassets and not _in_whitelist(rel_parts):
                continue

            rel_path = os.path.relpath(abs_path, root)
            imageset_dir = None
            if in_xcassets:
                parts = abs_path.split(os.sep)
                for idx, part in enumerate(parts):
                    if part.endswith('.imageset') or part.endswith('.appiconset'):
                        imageset_dir = os.sep.join(parts[: idx + 1])
                        imageset_count += 1
                        break

            images.append({
                'path': abs_path,
                'rel_path': rel_path,
                'in_xcassets': in_xcassets,
                'imageset_dir': imageset_dir,
                'extension': ext,
            })

    return {
        'project_root': root,
        'xcassets': sorted(set(xcassets_dirs)),
        'images': images,
        'counts': {
            'xcassets': len(xcassets_dirs),
            'images': len(images),
            'imagesets': imageset_count,
        },
        'ignore_dirs': sorted(ignored),
    }


def format_scan_log(scan_result):
    c = scan_result['counts']
    parts = []
    if c['xcassets']:
        parts.append(f'{c["xcassets"]} 个 .xcassets')
    if c['images']:
        parts.append(f'{c["images"]} 张图片')
    if not parts:
        return '未检测到 .xcassets 或图片资源'
    return '、'.join(parts)
