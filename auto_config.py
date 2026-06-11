# -*- coding: utf-8 -*-
import json
import os

from project_detect import DEFAULT_IGNORE_DIRS

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def auto_profile_path(profile_name):
    return os.path.join(REPO_ROOT, 'profiles', profile_name, 'auto.json')


def load_auto_settings(profile_name):
    defaults = {
        'enabled_modules': None,
        'ignore_dirs': sorted(DEFAULT_IGNORE_DIRS),
    }
    path = auto_profile_path(profile_name)
    if not os.path.isfile(path):
        return defaults
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if data.get('ignore_dirs'):
        defaults['ignore_dirs'] = data['ignore_dirs']
    if 'enabled_modules' in data:
        defaults['enabled_modules'] = data['enabled_modules']
    return defaults
