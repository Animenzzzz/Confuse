# -*- coding: utf-8 -*-
"""扫描 Xcode 工程目录，统计 OC / Swift 源文件并决定运行哪些模块。"""
import os

DEFAULT_IGNORE_DIRS = frozenset({
    'Pods',
    'Carthage',
    'Build',
    'build',
    '.git',
    'DerivedData',
    '.build',
    '3rd',
    'Index',
    '.svn',
    'node_modules',
    'Flutter',
    'ephemeral',
    '.symlinks',
    '.dart_tool',
})

ASSET_IMAGE_EXTENSIONS = frozenset({'.png', '.jpg', '.jpeg', '.webp'})

FLUTTER_MARKER_FILES = ('pubspec.yaml', 'pubspec.yml')
FLUTTER_AUX_DIRS = ('lib', 'android', 'web', 'linux', 'macos', 'windows')


def normalize_project_root(path):
    path = os.path.abspath(os.path.expanduser(path.strip()))
    if not os.path.isdir(path):
        raise FileNotFoundError(f'目录不存在: {path}')
    return path


def has_pubspec(directory):
    if not os.path.isdir(directory):
        return False
    for name in FLUTTER_MARKER_FILES:
        if os.path.isfile(os.path.join(directory, name)):
            return True
    return False


def find_xcodeproj(directory):
    """在目录的直接子项中查找 .xcodeproj（不递归）。"""
    if not os.path.isdir(directory):
        return None
    for name in sorted(os.listdir(directory)):
        if name.endswith('.xcodeproj'):
            return os.path.join(directory, name)
    return None


def _has_flutter_aux_markers(directory):
    return any(os.path.isdir(os.path.join(directory, name)) for name in FLUTTER_AUX_DIRS)


def _resolve_native_ios_root(path):
    xcodeproj = find_xcodeproj(path)
    return path, xcodeproj


def resolve_ios_root(project_path, native_only=False, flutter_settings=None):
    """
    解析实际 iOS 处理根路径。

    返回:
      input_path: 用户传入路径（绝对）
      ios_root: 扫描与混淆使用的 iOS 根目录
      project_kind: native | flutter | mixed
      flutter_root: Flutter 工程根（含 pubspec），无则为 None
      xcodeproj: 解析到的 .xcodeproj 绝对路径（可能为 None）
      ios_subpath: 配置中的 ios 子目录名
    """
    settings = flutter_settings or {}
    ios_subpath = settings.get('ios_subpath', 'ios')
    flutter_enabled = settings.get('flutter_enabled', True)

    input_path = normalize_project_root(project_path)
    base = {
        'input_path': input_path,
        'ios_subpath': ios_subpath,
    }

    if native_only or not flutter_enabled:
        ios_root, xcodeproj = _resolve_native_ios_root(input_path)
        return {
            **base,
            'ios_root': ios_root,
            'project_kind': 'native',
            'flutter_root': None,
            'xcodeproj': xcodeproj,
        }

    # 用户直接指向 ios/（或等价目录），且上级含 pubspec
    xcodeproj_at_input = find_xcodeproj(input_path)
    if xcodeproj_at_input and os.path.basename(input_path) == ios_subpath:
        parent = os.path.dirname(input_path)
        if has_pubspec(parent):
            return {
                **base,
                'ios_root': input_path,
                'project_kind': 'flutter',
                'flutter_root': parent,
                'xcodeproj': xcodeproj_at_input,
            }

    # Flutter 工程根：pubspec + ios/Runner.xcodeproj
    if has_pubspec(input_path):
        ios_dir = os.path.join(input_path, ios_subpath)
        xcodeproj = find_xcodeproj(ios_dir) if os.path.isdir(ios_dir) else None
        if xcodeproj:
            native_xcodeproj = find_xcodeproj(input_path)
            kind = 'mixed' if native_xcodeproj else 'flutter'
            return {
                **base,
                'ios_root': ios_dir,
                'project_kind': kind,
                'flutter_root': input_path,
                'xcodeproj': xcodeproj,
            }

    # 输入路径本身含 .xcodeproj → 纯原生
    if xcodeproj_at_input:
        return {
            **base,
            'ios_root': input_path,
            'project_kind': 'native',
            'flutter_root': None,
            'xcodeproj': xcodeproj_at_input,
        }

    # 无 pubspec 但存在 ios/ 子目录（混编 / 嵌套 iOS）
    ios_dir = os.path.join(input_path, ios_subpath)
    if os.path.isdir(ios_dir):
        xcodeproj = find_xcodeproj(ios_dir)
        if xcodeproj:
            kind = 'mixed'
            if has_pubspec(input_path) or _has_flutter_aux_markers(input_path):
                kind = 'flutter' if has_pubspec(input_path) else 'mixed'
            return {
                **base,
                'ios_root': ios_dir,
                'project_kind': kind,
                'flutter_root': input_path if has_pubspec(input_path) else None,
                'xcodeproj': xcodeproj,
            }

    ios_root, xcodeproj = _resolve_native_ios_root(input_path)
    return {
        **base,
        'ios_root': ios_root,
        'project_kind': 'native',
        'flutter_root': None,
        'xcodeproj': xcodeproj,
    }


def scan_project(project_root, ignore_dirs=None, resolution=None):
    """递归统计 .m / .h / .swift，跳过 ignore_dirs 中的目录名。"""
    root = normalize_project_root(project_root)
    ignored = set(DEFAULT_IGNORE_DIRS)
    if ignore_dirs:
        ignored.update(ignore_dirs)

    counts = {'m': 0, 'h': 0, 'swift': 0, 'xcassets': 0, 'images': 0}
    for dir_root, dirs, files in os.walk(root):
        dirs[:] = [
            d for d in dirs
            if d not in ignored and not d.endswith('.framework')
        ]
        for dirname in dirs:
            if dirname.endswith('.xcassets'):
                counts['xcassets'] += 1
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.m':
                counts['m'] += 1
            elif ext == '.h':
                counts['h'] += 1
            elif ext == '.swift':
                counts['swift'] += 1
            elif ext in ASSET_IMAGE_EXTENSIONS:
                counts['images'] += 1

    has_oc = counts['m'] > 0
    has_swift = counts['swift'] > 0
    has_assets = counts['xcassets'] > 0 or counts['images'] > 0
    result = {
        'project_root': root,
        'counts': counts,
        'has_oc': has_oc,
        'has_swift': has_swift,
        'has_assets': has_assets,
        'ignore_dirs': sorted(ignored),
    }
    if resolution:
        result['input_path'] = resolution['input_path']
        result['ios_root'] = resolution['ios_root']
        result['project_kind'] = resolution['project_kind']
        result['flutter_root'] = resolution.get('flutter_root')
        result['xcodeproj'] = resolution.get('xcodeproj')
    return result


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
            'assets': 'assets' in allowed,
        }
    return {
        'oc': detection['has_oc'],
        'swift': detection['has_swift'],
        'assets': detection['has_assets'],
    }


def _relative_display_path(path, base):
    try:
        rel = os.path.relpath(path, base)
        if rel == '.':
            return '.'
        if not rel.startswith('..'):
            return rel
    except ValueError:
        pass
    return path


def format_project_kind_log(resolution):
    kind = resolution.get('project_kind', 'native')
    ios_root = resolution['ios_root']
    input_path = resolution['input_path']
    ios_rel = _relative_display_path(ios_root, input_path)
    xcodeproj = resolution.get('xcodeproj')
    xcode_name = os.path.basename(xcodeproj) if xcodeproj else '(no .xcodeproj)'

    if kind == 'flutter':
        return f'Detected: Flutter project → iOS root: {ios_rel}/ ({xcode_name})'
    if kind == 'mixed':
        return f'Detected: Mixed project → iOS root: {ios_rel}/ ({xcode_name})'
    if ios_root != input_path:
        return f'Detected: Native project → iOS root: {ios_rel}/ ({xcode_name})'
    return f'Detected: Native project ({xcode_name})'


def format_detection_log(detection, modules):
    lines = []
    if detection.get('project_kind'):
        lines.append(format_project_kind_log(detection))
        if detection.get('flutter_root'):
            flutter_rel = _relative_display_path(
                detection['flutter_root'],
                detection['input_path'],
            )
            if flutter_rel == '.':
                lines.append(f'Flutter root: {detection["input_path"]}')
            else:
                lines.append(f'Flutter root: {flutter_rel}')

    c = detection['counts']
    parts = []
    if c['m'] or c['h']:
        parts.append(f'Objective-C ({c["m"]} .m, {c["h"]} .h)')
    if c['swift']:
        parts.append(f'Swift ({c["swift"]} files)')
    asset_parts = []
    if c.get('xcassets'):
        asset_parts.append(f'{c["xcassets"]} .xcassets')
    if c.get('images'):
        asset_parts.append(f'{c["images"]} images')
    if asset_parts:
        parts.append('Assets (' + ', '.join(asset_parts) + ')')
    if not parts:
        parts.append('未检测到 .m / .swift / 图片资源')

    run_parts = []
    if modules.get('assets'):
        run_parts.append('assets process')
    if modules['oc']:
        run_parts.append('OC writecode')
    if modules['swift']:
        run_parts.append('Swift writecontrol')
    run_text = '、'.join(run_parts) if run_parts else '无（请检查工程路径或 profile enabled_modules）'
    lines.append(f'Scanned: {", ".join(parts)} → running {run_text}')
    return '\n'.join(lines)
