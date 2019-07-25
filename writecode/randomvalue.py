# -*- coding: utf-8 -*-
import random
import sys
import re
import json
import string
import os

# 当前脚本工程的路径
confuse_path = f'{os.path.dirname(sys.path[0])}'
worlds_path = f"{confuse_path}/resource/words.txt"
ios_worlds_path = f"{confuse_path}/resource/ioswords.txt"

params_type_pool = ["int","float","void *","double","long long","bool","char"]

wfile = open(worlds_path,'r')
wstring = str(wfile.read())
worlds_arr = wstring.split(' ')
wfile.close()

iosfile = open(ios_worlds_path,'r')
iosstring = str(iosfile.read())
iosworlds_arr = iosstring.split(' ')
iosfile.close()

def type_value():
    index = random.randint(0,len(params_type_pool)-1)
    return params_type_pool[index]

def type_random_value(typevalue):
    if typevalue == "int" or typevalue == "float" or typevalue == "double" or typevalue == "long long":
        return int_value(1,1000)
    elif typevalue == "char":
        return f'\'{chr(random.randint(97, 122))}\''
    elif typevalue == "bool":
        return "YES"
    else:
        return "NULL"

def int_value(minv,maxv):
    return random.randint(minv,maxv)

def string_value():
    random_index = random.randint(0,len(worlds_arr)-1)
    random_world = worlds_arr[random_index]
    if random_world is None or random_world == "":
        string_value()
    else:
        return random_world

def string_ios_value():
    random_index = random.randint(0,len(iosworlds_arr)-1)
    random_world = iosworlds_arr[random_index]
    if random_world is None or random_world == "":
        string_value()
    else:
        return random_world

def string_value_num(num):
    random_world = ""
    for item in range(0,num):
        random_index = random.randint(0,len(worlds_arr)-1)
        world_tmp = worlds_arr[random_index]
        if world_tmp is None or world_tmp == "":
            random_world = ""
            break
        random_world = random_world + world_tmp
    if random_world is None or random_world == "":
        string_value_num(num)
    else:
        return random_world

def func_create(random_func_path, func_name_num,class_name,writeflag):
    func_dic = {}
    func_dic["params"] = []
    func_dic["descrip"] = []
    func_dic["class_name"] = class_name
    params_num = int_value(1,5)
    for k in range(0,params_num):
        func_dic["params"].append(type_value())
        func_dic["descrip"].append(string_value())
    func_dic["returntype"] = "void"
    # 这是之前的写法，使用三个随机的单词组成函数名
    # func_dic["funcname"] = stringvalue_num(func_name_num)
    func_dic["funcname"] = f'{string_value()}{string_ios_value()}'

    if writeflag == 1:
        jsonfile = open(random_func_path,'a+')
        jsonfile.writelines(json.dumps(func_dic)+'\n')
        jsonfile.close()

    return func_dic

def half_probability():
    intnum = random.randint(1,2)
    if intnum == 1:
        return 1
    else:
        return 2