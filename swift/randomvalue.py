# -*- coding: utf-8 -*-
import importlib.util
import os

_writecode_randomvalue = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'writecode',
    'randomvalue.py',
)
_spec = importlib.util.spec_from_file_location('wc_randomvalue', _writecode_randomvalue)
_wc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_wc)

half_probability = _wc.half_probability
int_value = _wc.int_value
string_ios_value = _wc.string_ios_value
string_value = _wc.string_value
string_value_num = _wc.string_value_num

SWIFT_PARAM_TYPES = ['Int', 'Double', 'Bool', 'String', 'CGFloat']


def swift_type_value():
    return SWIFT_PARAM_TYPES[int_value(0, len(SWIFT_PARAM_TYPES) - 1)]


def swift_type_default(type_name):
    if type_name == 'Int':
        return str(int_value(0, 1000))
    if type_name in ('Double', 'CGFloat'):
        return f'{int_value(1, 100)}.{int_value(0, 99)}'
    if type_name == 'Bool':
        return 'true' if half_probability() == 1 else 'false'
    if type_name == 'String':
        return f'"{string_value()}"'
    return '0'


def swift_func_create(class_name=None, write_path=None):
    import json

    params = []
    param_count = int_value(0, 3)
    for _ in range(param_count):
        label = string_value()
        params.append({
            'label': label,
            'type': swift_type_value(),
            'external': label if int_value(0, 1) else '_',
        })

    func_dic = {
        'funcname': f'{string_value()}{string_ios_value()}',
        'params': params,
        'class_name': class_name or '',
        'returntype': 'Void',
    }

    if write_path:
        with open(write_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(func_dic) + '\n')

    return func_dic
