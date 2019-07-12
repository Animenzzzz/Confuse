# -*- coding: utf-8 -*-
import sys
import os

import randomvalue

if_num_min = 1
if_num_max = 5

switch_num_min = 1
switch_num_max = 5

func_num_min = 1
func_num_max = 5

def if_model():

    param_name = randomvalue.stringvalue()
    param_value = randomvalue.intvalue(0,1000)
    if_string = f"\tint {param_name} = {param_value};\n"

    #if的分支数
    random_num = randomvalue.intvalue(if_num_min,if_num_max)
    print("生成的随机数："+str(random_num))
    if random_num == 1:
        inline_string = inline_model()
        if_string = if_string + "\tif ("+param_name+" <= 1000){\n"+inline_string+"\t}\n"
        print("111111111")
    elif random_num == 2:
        inline_string1 = inline_model()
        inline_string2 = inline_model()
        if_string = if_string + "\tif ("+param_name+" <= 500){\n"+inline_string1+"\t}else{\n"+inline_string2+"\t}\n"
        print("2222222")
    else:
        level = 1000/random_num
        for num in range(1,random_num+1):
            if num == 1:
                inline_string = inline_model()
                if_string = if_string + "\tif ("+param_name+" <= "+str(level*num)+"){\n"+inline_string+"\t}\n"
            elif num == random_num:
                inline_string = inline_model()
                if_string = if_string + "\telse{\n"+inline_string+"\t}\n"
            else:
                inline_string = inline_model()
                if_string = if_string + "\telse if("+param_name+" > "+str(level*(num-1))+" && "+param_name+" =< "+str(level*num)+"){\n"+inline_string+"\t}\n"
    return if_string

def switch_model():
    return "kihafdsdkifhasik"

def func_model():
    return "kihafdsdkifhasik"

def while_model():
    return "kihafdsdkifhasik"

def inline_model():
    param_name = randomvalue.stringvalue()
    param_value = randomvalue.stringvalue()
    result_string = "\t\tNSString *"+param_name+" = @\""+param_value+"\";\n"+"\t\tNSLog(\"%@\", "+param_name+");\n"
    return result_string