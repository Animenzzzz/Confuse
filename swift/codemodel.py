# -*- coding: utf-8 -*-
import randomvalue

TAB = '    '

PROPERTY_TEMPLATES = [
    ('var', 'Int', '0'),
    ('var', 'String', '""'),
    ('var', 'Bool', 'false'),
    ('var', 'Double', '0.0'),
    ('var', 'CGFloat', '0.0'),
    ('let', 'String', '""'),
    ('var', '[String]', '[]'),
    ('var', 'Int?', 'nil'),
]

SUPER_TYPES = [
    ('UIViewController', 'UIKit'),
    ('UIView', 'UIKit'),
    ('UITableViewCell', 'UIKit'),
    ('UICollectionViewCell', 'UIKit'),
    ('NSObject', 'Foundation'),
]

FILE_SUFFIXES = ['ViewController', 'View', 'Cell', 'Manager', 'Handler', 'Service']


def property_model(num_min, num_max):
    count = randomvalue.int_value(num_min, num_max)
    lines = []
    for _ in range(count):
        kind, type_name, default = PROPERTY_TEMPLATES[randomvalue.int_value(0, len(PROPERTY_TEMPLATES) - 1)]
        name = randomvalue.string_value_num(2)
        first = name[0].lower() + name[1:] if name else 'item'
        lines.append(f'{TAB}private {kind} {first}: {type_name} = {default}')
    return '\n'.join(lines) + '\n'


def inline_body():
    var_name = randomvalue.string_value()
    value = randomvalue.string_value()
    return (
        f'{TAB}{TAB}let {var_name} = "{value}"\n'
        f'{TAB}{TAB}print({var_name})\n'
    )


def if_block():
    var_name = randomvalue.string_value()
    threshold = randomvalue.int_value(100, 900)
    return (
        f'{TAB}{TAB}let {var_name} = {randomvalue.int_value(0, 1000)}\n'
        f'{TAB}{TAB}if {var_name} > {threshold} {{\n'
        f'{inline_body()}'
        f'{TAB}{TAB}}}\n'
    )


def func_signature(func_dic, visibility='private'):
    name = func_dic['funcname']
    params = func_dic['params']
    if not params:
        return f'{TAB}{visibility} func {name}()'
    parts = []
    for index, param in enumerate(params):
        external = param['external']
        label = param['label']
        type_name = param['type']
        if index == 0 and external == '_':
            parts.append(f'_ {label}: {type_name}')
        elif external == '_':
            parts.append(f'_ {label}: {type_name}')
        else:
            parts.append(f'{external} {label}: {type_name}')
    return f'{TAB}{visibility} func {name}({", ".join(parts)})'


def func_model(func_dic, visibility='private'):
    body = inline_body()
    if randomvalue.half_probability() == 1:
        body = if_block()
    return f'\n{func_signature(func_dic, visibility)} {{\n{body}{TAB}}}\n'


def func_call_model(func_dic, visibility=''):
    class_name = func_dic.get('class_name') or ''
    instance = randomvalue.string_value()
    args = []
    for param in func_dic['params']:
        external = param['external']
        label = param['label']
        value = randomvalue.swift_type_default(param['type'])
        if external == '_':
            args.append(f'{value}')
        else:
            args.append(f'{label}: {value}')
    arg_string = ', '.join(args)
    if class_name:
        call = f'let {instance} = {class_name}()\n{TAB}{instance}.{func_dic["funcname"]}({arg_string})'
    else:
        call = f'{func_dic["funcname"]}({arg_string})'
    if visibility:
        call = f'{TAB}{call}'
    return f'\n{call}\n'


def new_class_name():
    return f'{randomvalue.string_value()}{randomvalue.string_ios_value()}{FILE_SUFFIXES[randomvalue.int_value(0, len(FILE_SUFFIXES) - 1)]}'


def new_file_content(class_name, member_min, member_max, super_type=None):
    if super_type is None:
        super_type, module = SUPER_TYPES[randomvalue.int_value(0, len(SUPER_TYPES) - 1)]
    else:
        module = 'UIKit' if super_type in ('UIViewController', 'UIView', 'UITableViewCell', 'UICollectionViewCell') else 'Foundation'

    lines = [
        f'import {module}',
        '',
        f'final class {class_name}: {super_type} {{',
        '',
    ]

    prop_block = property_model(member_min, member_max).rstrip()
    if prop_block:
        lines.append(prop_block)
        lines.append('')

    func_count = randomvalue.int_value(member_min, member_max)
    for _ in range(func_count):
        func_dic = randomvalue.swift_func_create(class_name)
        lines.append(func_model(func_dic).strip())
        lines.append('')

    lines.append('}')
    lines.append('')
    return '\n'.join(lines)


def call_all_file_content(class_name, func_name):
    return (
        f'import Foundation\n\n'
        f'final class {class_name} {{\n'
        f'{TAB}static let shared = {class_name}()\n'
        f'{TAB}private init() {{}}\n\n'
        f'{TAB}func {func_name}() {{\n'
        f'{TAB}}}\n'
        f'}}\n'
    )
