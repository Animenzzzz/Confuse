# -*- coding: utf-8 -*-
"""图片指纹差异化：重编码、像素扰动、metadata 剥离。"""
import hashlib
import os
import random
import shutil
import subprocess
import tempfile

import config

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:12]


def _sips_reencode(src, dst, quality):
    ext = os.path.splitext(src)[1].lower()
    fmt_map = {'.png': 'png', '.jpg': 'jpeg', '.jpeg': 'jpeg', '.webp': 'webp'}
    fmt = fmt_map.get(ext)
    if not fmt:
        return False
    tmp = dst + '.tmp'
    shutil.copy2(src, tmp)
    try:
        subprocess.run(
            ['sips', '-s', 'format', fmt, '-s', 'formatOptions', str(quality), tmp, '--out', dst],
            check=True,
            capture_output=True,
        )
        os.remove(tmp)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        if os.path.isfile(tmp):
            os.remove(tmp)
        return False


def _pillow_reencode(src, dst, quality, strip_meta, perturb):
    ext = os.path.splitext(src)[1].lower()
    img = Image.open(src)
    if perturb and config.perturb_enabled and config.operation_enabled('perturb'):
        img = _apply_perturb(img)

    save_kwargs = {}
    if ext in ('.jpg', '.jpeg'):
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
        if strip_meta:
            save_kwargs['exif'] = b''
    elif ext == '.png':
        save_kwargs['optimize'] = True
    elif ext == '.webp':
        save_kwargs['quality'] = quality

    fmt = {'.png': 'PNG', '.jpg': 'JPEG', '.jpeg': 'JPEG', '.webp': 'WEBP'}.get(ext, 'PNG')
    img.save(dst, format=fmt, **save_kwargs)
    return True


def _apply_perturb(img):
    strength = max(1, min(config.perturb_strength, 3))
    if img.mode not in ('RGB', 'RGBA', 'L'):
        img = img.convert('RGBA' if 'A' in img.mode else 'RGB')

    pixels = img.load()
    width, height = img.size
    if width == 0 or height == 0:
        return img

    sample_count = max(1, (width * height) // 10000)
    for _ in range(sample_count):
        x = random.randrange(width)
        y = random.randrange(height)
        px = pixels[x, y]
        if isinstance(px, int):
            delta = random.randint(-strength, strength)
            pixels[x, y] = max(0, min(255, px + delta))
        else:
            channels = list(px)
            for i in range(len(channels) - (1 if img.mode == 'RGBA' else 0)):
                delta = random.randint(-strength, strength)
                channels[i] = max(0, min(255, channels[i] + delta))
            pixels[x, y] = tuple(channels)
    return img


def process_image(src_path, dst_path, dry_run=False):
    """
    对单张图片执行已启用操作，返回操作描述列表。
    dst_path 可与 src_path 相同（原地）。
    """
    ops = []
    if config.operation_enabled('reencode'):
        ops.append('reencode')
    if config.operation_enabled('strip_metadata'):
        ops.append('strip_metadata')
    if config.operation_enabled('perturb') and config.perturb_enabled:
        ops.append('perturb')

    if not ops:
        return []

    if dry_run:
        return ops

    quality = config.reencode_quality
    strip_meta = config.operation_enabled('strip_metadata')
    perturb = config.operation_enabled('perturb') and config.perturb_enabled

    os.makedirs(os.path.dirname(dst_path) or '.', exist_ok=True)
    same_file = os.path.abspath(src_path) == os.path.abspath(dst_path)

    if HAS_PILLOW:
        if same_file:
            fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(src_path)[1])
            os.close(fd)
            try:
                _pillow_reencode(src_path, tmp, quality, strip_meta, perturb)
                shutil.move(tmp, dst_path)
            except Exception:
                if os.path.isfile(tmp):
                    os.remove(tmp)
                raise
        else:
            _pillow_reencode(src_path, dst_path, quality, strip_meta, perturb)
        return ops

    if config.operation_enabled('reencode') and shutil.which('sips'):
        if same_file:
            fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(src_path)[1])
            os.close(fd)
            try:
                ok = _sips_reencode(src_path, tmp, quality)
                if ok:
                    shutil.move(tmp, dst_path)
                else:
                    os.remove(tmp)
            except Exception:
                if os.path.isfile(tmp):
                    os.remove(tmp)
                raise
        else:
            _sips_reencode(src_path, dst_path, quality)
        if perturb:
            print('  警告：未安装 Pillow，已跳过像素扰动（perturb）')
        return ops

    if perturb:
        print('  警告：未安装 Pillow 且无 sips，仅跳过 perturb/reencode')
    return []


def copy_project_tree(src_root, dst_root):
    """非原地模式：复制工程到输出目录（跳过 ignore_dirs）。"""
    ignored = set(config.ignore_dirs)
    from project_detect import DEFAULT_IGNORE_DIRS
    ignored.update(DEFAULT_IGNORE_DIRS)

    for dir_root, dirs, files in os.walk(src_root):
        rel = os.path.relpath(dir_root, src_root)
        dirs[:] = [d for d in dirs if d not in ignored and not d.endswith('.framework')]
        out_dir = dst_root if rel == '.' else os.path.join(dst_root, rel)
        os.makedirs(out_dir, exist_ok=True)
        for filename in files:
            src = os.path.join(dir_root, filename)
            dst = os.path.join(out_dir, filename)
            if not os.path.isfile(dst):
                shutil.copy2(src, dst)
