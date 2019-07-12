# -*- coding: utf-8 -*-
import random
import sys
import re

worlds_path = "/Users/animenzzz/GitCode/Confuse/resource/words.txt"

def intvalue(minv,maxv):
    return random.randint(minv,maxv)

def stringvalue():
    wfile = open(worlds_path,'r')
    wstring = str(wfile.read())
    worlds_arr = wstring.split(' ')
    random_index = random.randint(0,len(worlds_arr))
    random_world = worlds_arr[random_index]
    wfile.close()
    return random_world

def stringvalue_num(num):
    wfile = open(worlds_path,'r')
    wstring = str(wfile.read())
    worlds_arr = wstring.split(' ')
    random_world = ""
    for item in range(0,num):
        random_index = random.randint(0,len(worlds_arr))
        random_world = random_world + worlds_arr[random_index]
    wfile.close()
    return random_world
