# -*- coding: utf-8 -*-
import json
import os

from project_detect import DEFAULT_IGNORE_DIRS

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def _profile_json_path(profile_name, filename):
    return os.path.join(REPO_ROOT, 'profiles', profile_name, filename)


def auto_profile_path(profile_name):
    return _profile_json_path(profile_name, 'auto.json')


def flutter_profile_path(profile_name):
    return _profile_json_path(profile_name, 'flutter.json')


def load_flutter_settings(profile_name):
    defaults = {
        'flutter_enabled': True,
        'ios_subpath': 'ios',
        'ignore_dirs': ['Pods', 'Flutter', 'build', '.symlinks', 'ephemeral', '.dart_tool'],
        'runner_target': 'Runner',
        'recommended_file_while_list': ['Runner', 'Classes'],
    }
    path = flutter_profile_path(profile_name)
    if not os.path.isfile(path):
        return defaults
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for key in defaults:
        if key in data:
            defaults[key] = data[key]
    return defaults


def load_auto_settings(profile_name):
    defaults = {
        'enabled_modules': None,
        'ignore_dirs': sorted(DEFAULT_IGNORE_DIRS),
        'assets_enabled': True,
    }
    path = auto_profile_path(profile_name)
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        if data.get('ignore_dirs'):
            defaults['ignore_dirs'] = data['ignore_dirs']
        if 'enabled_modules' in data:
            defaults['enabled_modules'] = data['enabled_modules']
        if 'assets_enabled' in data:
            defaults['assets_enabled'] = data['assets_enabled']

    flutter = load_flutter_settings(profile_name)
    defaults['flutter'] = flutter
    if flutter.get('ignore_dirs'):
        merged = set(defaults['ignore_dirs'])
        merged.update(flutter['ignore_dirs'])
        defaults['ignore_dirs'] = sorted(merged)
    return defaults
