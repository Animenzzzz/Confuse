# -*- coding: utf-8 -*-
import json
import os


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def profile_dir(profile_name):
    return os.path.join(repo_root(), 'profiles', profile_name)


def assets_profile_path(profile_name):
    return os.path.join(profile_dir(profile_name), 'assets.json')


def load_assets_settings(profile_name):
    path = assets_profile_path(profile_name)
    if not os.path.isfile(path):
        raise FileNotFoundError(
            'Profile assets config not found: %s (try profiles/%s/assets.json)'
            % (path, profile_name)
        )
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def resolve_profile_name(argv=None):
    profile = os.environ.get('CONFUSE_PROFILE', 'default')
    if argv is None:
        return profile

    index = 0
    while index < len(argv):
        item = argv[index]
        if item == '--profile' and index + 1 < len(argv):
            profile = argv[index + 1]
            del argv[index:index + 2]
            continue
        if item.startswith('--profile='):
            profile = item.split('=', 1)[1]
            del argv[index]
            continue
        index += 1
    return profile
