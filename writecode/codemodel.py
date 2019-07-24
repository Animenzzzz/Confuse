# -*- coding: utf-8 -*-
import sys
import os
import randomvalue
import re
import json


if_num_min = 1
if_num_max = 5

#最小值不能修改！！！
switch_num_min = 2
switch_num_max = 5

func_num_min = 1
func_num_max = 5

tab_level_1 = "\t"
tab_level_2 = "\t\t"
tab_level_3 = "\t\t\t"


property_list = [\
"@property (nonatomic, assign) int ",\
"@property (nonatomic, assign) NSInteger ",\
"@property (nonatomic, assign) long ",\
"@property (nonatomic, assign) long long ",\
"@property (nonatomic, assign) CGFloat ",\
"@property (nonatomic, assign) double ",\
"@property (nonatomic, assign) BOOL ",\
"@property (nonatomic, assign) CGRect ",\
"@property (nonatomic, assign) CGSize ",\
"@property (nonatomic, copy) id ",\
"@property (nonatomic, strong) id ",\
"@property (nonatomic, weak) id "
]


def _inline_model_tablevel(tablevel):
    if tablevel is None:
        tablevel = tab_level_1
    param_name = randomvalue._string_value()
    param_value = randomvalue._string_value()
    result_string = f'{tablevel}NSString *{param_name} = @\"{param_value}\";\n{tablevel}NSLog(@\"%@\", {param_name});\n'
    return result_string

def _if_model(tablevel):

    if tablevel is None:
        tablevel = tab_level_1

    param_name = randomvalue._string_value_num(2)
    param_value = randomvalue._int_value(0,1000)
    param_name_selfid = randomvalue._string_value_num(3)
    if_string = f"{tablevel}id {param_name_selfid} = self;\n{tablevel}int {param_name} = [{param_name_selfid} intValue];\n"

    #if的分支数
    random_num = randomvalue._int_value(if_num_min,if_num_max)

    if random_num == 1:
        inline_string = _inline_model_tablevel(tab_level_2)
        if_string = f'{if_string}{tablevel}if ({param_name} <= 1000){{\n{inline_string}\t}}\n'
    elif random_num == 2:
        inline_string1 = _inline_model_tablevel(tab_level_2)
        inline_string2 = _inline_model_tablevel(tab_level_2)
        if_string = f'{if_string}{tablevel}if ({param_name} <= 500){{\n{inline_string1}\t}}else{{\n{inline_string2}\t}}\n'
    else:
        level = 1000/random_num
        for num in range(1,random_num+1):
            if num == 1:
                inline_string = _inline_model_tablevel(tab_level_2)
                level_num_str = str(level*num)
                if_string = f'{if_string}{tablevel}if ({param_name} <= {level_num_str}){{\n{inline_string}\t}}\n'
            elif num == random_num:
                inline_string = _inline_model_tablevel(tab_level_2)
                if_string = f'{if_string}{tablevel}else{{\n{inline_string}\t}}\n'
            else:
                inline_string = _inline_model_tablevel(tab_level_2)
                level_num_str = str(level*(num-1))
                level_num_str1 = str(level*num)
                if_string = f'{if_string}{tablevel}else if({param_name} > {level_num_str} && {param_name} <= {level_num_str1}){{\n{inline_string}\t}}\n'
    return f'\n{if_string}\n'

def _switch_model(tablevel):

    if tablevel is None:
        tablevel = tab_level_1

    param_name = randomvalue._string_value()
    param_value = randomvalue._int_value(switch_num_min,switch_num_max)
    param_name_selfid = randomvalue._string_value_num(3)
    switch_string = f"{tablevel}id {param_name_selfid} = self;\n{tablevel}int {param_name} = [{param_name_selfid} intValue];\n"
    # switch_string = f"{tablevel}int {param_name} = {param_value};\n"

    #switch的分支数
    random_num = randomvalue._int_value(switch_num_min,switch_num_max)
    randstring1 = randomvalue._string_value()
    if random_num == switch_num_min:
        inline_string1 = _inline_model_tablevel(tab_level_3)
        switch_string = f'{switch_string}{tablevel}switch ({param_name}) {{\n{tablevel}{tab_level_1}case 2:{{\n{inline_string1}{tablevel}{tab_level_2}}}break;\n{tablevel}{tab_level_1}default:{{\n{tablevel}{tab_level_2}NSLog(@\"do not catch anything\");\n{tablevel}{tab_level_2}}}break;\n\t}}\n'
    else:
        for num in range(switch_num_min,random_num+1):
            if num == switch_num_min:
                inline_string1 = _inline_model_tablevel(tab_level_3)
                switch_string = f'{switch_string}{tablevel}switch ({param_name}) {{\n{tablevel}{tab_level_1}case 2:{{\n{inline_string1}{tablevel}{tab_level_2}}}break;\n'
            elif num == random_num:
                switch_string = f'{switch_string}\n{tablevel}{tab_level_1}default:\n{tablevel}{tab_level_2}{{NSLog(@\"do not catch anything\");\n{tablevel}{tab_level_2}}}break;\n\t}}\n'
            else:
                inline_string1 = _inline_model_tablevel(tab_level_3)
                num_str = str(num)
                switch_string = f'\n{switch_string}\n{tablevel}{tab_level_1}case {num_str}:{{\n{inline_string1}{tablevel}{tab_level_2}}}break;'
    return f'\n{switch_string}\n'

# 自定义函数的调用
def _constom_func_call_model(funcjsonstring,tablevel):
    funcdic = eval(funcjsonstring)
    if funcdic["funcname"] == "":
        print("函数名为空")
        return
    obj_name = randomvalue._string_value()
    class_type = funcdic["class_name"]

    func_string = ""
    func_string = f'{tab_level_1}{class_type} *{obj_name} = [{class_type} new];\n'

    params_name = []
    for i in range(0,len(funcdic["params"])):
        params_name.append(randomvalue._string_value_num(2))

    param_init_string = ""
    for i in range(len(funcdic["params"])):
        param_init_string = f'{param_init_string}{tab_level_1}{funcdic["params"][i]} {params_name[i]} = {randomvalue._type_random_value(funcdic["params"][i])};\n'


    call_string = ""
    if len(params_name) == 0:
        call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}];\n'
    else:
        if len(funcdic["descrip"]) == 1:
            call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}:{params_name[0]}];\n'
        else:
            call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}:{params_name[0]} '
            for i in range(1,len(funcdic["descrip"])):
                call_string = f'{call_string}{funcdic["descrip"][i]}:{params_name[i]} '
            call_string = f'{call_string}];\n'

    return f'\n{func_string}{param_init_string}{call_string}\n'

# 系统函数的调用
def _system_func_call_model(funcjsonstring,tablevel):

    funcdic = eval(funcjsonstring)
    if funcdic["funcname"] == "":
        print("函数名为空")
        return
    class_name = randomvalue._string_value()
    class_string = randomvalue._string_value()

    func_string = ""
    func_string = f'{tab_level_1}Class {class_name} = NSClassFromString(@\"{class_string}\");\n'

    msg_send_param = ""
    param_string = ""
    param_descri_string = ""
    imp_string = ""
    sel_name = randomvalue._string_value()
    imp_name = randomvalue._string_value()
    if len(funcdic["params"]):
        for i in range(len(funcdic["params"])):
            param_name = randomvalue._string_value()
            param_string = f'{param_string}{tab_level_1}id {param_name};\n'
            msg_send_param = f'{msg_send_param},{param_name}'
            imp_string = f'{imp_string},id'
            if i != 0:
                param_descri_string = f'{param_descri_string}:{funcdic["descrip"][i-1]}'
        if param_descri_string == "":
            param_descri_string = ":"
        sel_string = f'{tab_level_1}SEL {sel_name} = @selector({funcdic["funcname"]}{param_descri_string}:);\n'
        func_string = f'{func_string}{param_string}{sel_string}'
    else:
        sel_string = f'{tab_level_1}SEL {sel_name} = @selector({funcdic["funcname"]});\n'
        func_string = f'{func_string}{sel_string}'

    # objc_msgSend 的写法
    # func_string = f'{func_string}{tab_level_1}objc_msgSend({class_name},{sel_name}{msg_send_param});'
    # func_string = str(func_string).replace("::",":")
    # performSelector 的写法
    # func_string = f'{func_string}{tab_level_1}[{class_name} performSelector:{sel_name} withObject:{msg_send_param}];'
    # func_string = str(func_string).replace("::",":").replace(":,",":")
    # imp 的写法
    imp_init_string = f'IMP {imp_name} = [{class_name} methodForSelector:{sel_name}];'
    func_string = f'{func_string}{tab_level_1}{imp_init_string}\n{tab_level_1}((id(*)(id, SEL{imp_string})){imp_name})({class_name},{sel_name}{msg_send_param});'
    func_string = str(func_string).replace("::",":")
    return f'\n{func_string}\n'

# 自定义函数的声明
def _constom_func_head_model(funcdic):

    func_head_string = ""
    func_head_string = f'- (void) {funcdic["funcname"]}:({funcdic["params"][0]}){funcdic["descrip"][0]}'

    descrp_string = ""
    for j in range(1,len(funcdic["descrip"])):
        descrp_string = f'{descrp_string} {funcdic["descrip"][j]}:({funcdic["params"][j]}){funcdic["descrip"][j]}'

    return f'\n{func_head_string}{descrp_string}'

# 自定义函数的实现
def _func_model(if_model_flag, while_model_flag, switch_model_flag, func_call_string_array, tablevel,func_dic):

    if_string = ""
    if if_model_flag == 1:
        if_string = _if_model(None)
    
    while_string = ""
    if while_model_flag == 1:
        while_string = _while_model(None)

    switch_string = ""
    if switch_model_flag == 1:
        switch_string = _switch_model(None)

    func_call_string = ""
    if len(func_call_string_array):
        for item in func_call_string_array:
            func_call_string_item = _system_func_call_model(str(item).strip('\n'), tablevel)
            if func_call_string_item is None:
                func_call_string_item = " "
            func_call_string = f'{func_call_string}{func_call_string_item}'

    if func_call_string == "":
        func_call_string = " "
    
    func_head_string = _constom_func_head_model(func_dic)

    # 每个模块随机乱序
    random_sort = randomvalue._int_value(1,4)
    if random_sort == 1:
        func_create_string = f'{func_head_string}{{\n{if_string}{while_string}{switch_string}{func_call_string}}}'
    elif random_sort == 2:
        func_create_string = f'{func_head_string}{{\n{while_string}{switch_string}{if_string}{func_call_string}}}'
    elif random_sort == 3:
        func_create_string = f'{func_head_string}{{\n{func_call_string}{while_string}{if_string}{switch_string}}}'
    else:
        func_create_string = f'{func_head_string}{{\n{switch_string}{func_call_string}{if_string}{while_string}}}'

    return f'\n{func_create_string}\n'

def _while_model(tablevel):

    if tablevel is None:
        tablevel = tab_level_1
    inline_string = _inline_model_tablevel(tab_level_2)
    while_string = f'\n{tablevel}while(1){{\n{inline_string}\n{tablevel}break;\n{tablevel}}}\n'
    return while_string

def _property_model(num_min,num_max):
    totle = randomvalue._int_value(num_min,num_max)
    property_string = ""
    for i in range(totle):
        index = randomvalue._int_value(0,len(property_list)-1)
        property_name = randomvalue._string_value_num(2)
        property_string = f'{property_string}{property_list[index]}{property_name};\n'

    return property_string