# -*- coding: utf-8 -*-
import os

import profile_loader

IMAGE_EXTENSIONS = frozenset({'.png', '.jpg', '.jpeg', '.webp'})

file_while_list = []
scan_whole_project = True
enabled_operations = ['reencode', 'strip_metadata']
skip_patterns = ['AppIcon', 'LaunchImage', 'LaunchScreen']
ignore_dirs = []
in_place = True
output_suffix = '_assets_out'
copy_to = ''
reencode_quality = 95
perturb_enabled = False
perturb_strength = 1
rename_assets = False
rename_prefix = 'img_'
randomize_imageset_filenames = False
active_profile = 'default'

project_root = ''


def load_profile(profile_name=None):
    global file_while_list, scan_whole_project, enabled_operations
    global skip_patterns, ignore_dirs, in_place, output_suffix, copy_to
    global reencode_quality, perturb_enabled, perturb_strength
    global rename_assets, rename_prefix, randomize_imageset_filenames
    global active_profile

    if profile_name is None:
        profile_name = os.environ.get('CONFUSE_PROFILE', 'default')

    settings = profile_loader.load_assets_settings(profile_name)
    file_while_list = settings.get('file_while_list', [])
    scan_whole_project = settings.get('scan_whole_project', True)
    enabled_operations = settings.get('enabled_operations', ['reencode', 'strip_metadata'])
    skip_patterns = settings.get('skip_patterns', ['AppIcon', 'LaunchImage', 'LaunchScreen'])
    ignore_dirs = settings.get('ignore_dirs', [])
    in_place = settings.get('in_place', True)
    output_suffix = settings.get('output_suffix', '_assets_out')
    copy_to = settings.get('copy_to', '')
    reencode_quality = settings.get('reencode_quality', 95)
    perturb_enabled = settings.get('perturb_enabled', False)
    perturb_strength = settings.get('perturb_strength', 1)
    rename_assets = settings.get('rename_assets', False)
    rename_prefix = settings.get('rename_prefix', 'img_')
    randomize_imageset_filenames = settings.get('randomize_imageset_filenames', False)
    active_profile = profile_name
    os.environ['CONFUSE_PROFILE'] = profile_name


load_profile()


def set_project_root(path):
    global project_root
    project_root = path


def get_project_root():
    return project_root


def operation_enabled(name):
    return name in enabled_operations


def resolve_output_root():
    """根据 in_place / copy_to / output_suffix 决定实际处理的根目录。"""
    if copy_to:
        return os.path.abspath(os.path.expanduser(copy_to))
    if in_place:
        return get_project_root()
    return get_project_root() + output_suffix
