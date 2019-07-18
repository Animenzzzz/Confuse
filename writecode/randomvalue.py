# -*- coding: utf-8 -*-
import random
import sys
import re
import json
import string

worlds_path = "/Users/animenzzz/GitCode/Confuse/resource/words.txt"

params_type_pool = ["int","float","void *","double","long long","bool","char"]

wfile = open(worlds_path,'r')
wstring = str(wfile.read())
worlds_arr = wstring.split(' ')
wfile.close()

def typevalue():
    index = random.randint(0,len(params_type_pool)-1)
    return params_type_pool[index]

def typerandomvalue(typevalue):
    if typevalue == "int" or typevalue == "float" or typevalue == "double" or typevalue == "long long":
        return intvalue(1,1000)
    elif typevalue == "char":
        return f'\'{chr(random.randint(97, 122))}\''
    elif typevalue == "bool":
        return "YES"
    else:
        return "NULL"

def intvalue(minv,maxv):
    return random.randint(minv,maxv)

def stringvalue():
    random_index = random.randint(0,len(worlds_arr)-1)
    random_world = worlds_arr[random_index]
    if random_world is None or random_world == "":
        stringvalue()
    else:
        return random_world

def stringvalue_num(num):
    random_world = ""
    for item in range(0,num):
        random_index = random.randint(0,len(worlds_arr)-1)
        world_tmp = worlds_arr[random_index]
        if world_tmp is None or world_tmp == "":
            random_world = ""
            break
        random_world = random_world + world_tmp
    if random_world is None or random_world == "":
        stringvalue_num(num)
    else:
        return random_world

def funccreate(random_func_path, func_name_num,class_name):
    func_dic = {}
    func_dic["params"] = []
    func_dic["descrip"] = []
    func_dic["class_name"] = class_name
    params_num = intvalue(1,5)
    for k in range(0,params_num):
        func_dic["params"].append(typevalue())
        func_dic["descrip"].append(stringvalue())
    func_dic["returntype"] = "void"
    func_dic["funcname"] = stringvalue_num(func_name_num)

    jsonfile = open(random_func_path,'a+')
    jsonfile.writelines(json.dumps(func_dic)+'\n')
    jsonfile.close()

    return func_dic

def halfprobability():
    intnum = random.randint(1,2)
    if intnum == 1:
        return 1
    else:
        return 2