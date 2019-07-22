# -*- coding: utf-8 -*-
import sys
import os
import randomvalue
import re
import json

file_type_pool = ["UIViewController","NSObject","UIView","UICollectionViewCell","UICollectionViewController","UITableViewCell","UITableViewController"]
file_name_pool = ["ViewController","Obj","View","CollectionViewCell","CollectionController","Cell","TableViewController"]

def create_h_m(outpath,name):

    super_class = "NSObject"
    if name is None:
        index = randomvalue.intvalue(0,len(file_type_pool)-1)
        world = randomvalue.stringvalue()
        name = f'{world}{file_name_pool[index]}'
        super_class = f'{file_type_pool[index]}'

    newfile_h = open(f'{outpath}/{name}.h','w')
    h_string = f'#import <UIKit/UIKit.h>\nNS_ASSUME_NONNULL_BEGIN\n\n@interface {name} : {super_class}\n\n@end\n\nNS_ASSUME_NONNULL_END'
    newfile_h.write(h_string)
    newfile_h.close()

    newfile_m = open(f'{outpath}/{name}.m','w')
    m_string = f'#import \"{name}.h\"\n#import <objc/message.h>\n@implementation {name}\n\n@end'
    newfile_m.write(m_string)
    newfile_m.close()
    print(f'生成类：{name}')

    path_dir = {"m_path":f'{outpath}/{name}.m',"h_path":f'{outpath}/{name}.h',"class_name":f'{name}'}

    
    return path_dir

def findkeyline(filepath,keyworld):
    for count,line in enumerate(open(filepath,'r')):
        if keyworld in line and line.find(f'//{keyworld}') == -1:
            return count

def getwhitefile(filepath,whitelist):
    resultlist = []
    for path,group_list,file_name_list in os.walk(filepath):
        for group_item in group_list:
            if group_item in whitelist:
                for path1,group_list1,file_name_list1 in os.walk(os.path.join(path, group_item)):
                    for item in file_name_list1:
                        resultlist.append(os.path.join(path, group_item,item))
    return resultlist

def writestring(filepath,string,line_num):

    if line_num is None:
        line_num = 0
        if os.path.splitext(filepath)[-1] == '.h':
            line_num = 5
        else:
            line_num = 4

    lines=[]
    writefile = open(filepath,'r')
    for line in writefile:
        lines.append(line)
    writefile.close()
 
    lines.insert(line_num,string)
    s = "".join('%s' %id for id in lines)
    writefile = open(filepath,'w+')
    writefile.write(s)
    writefile.close()
    del lines[:]
