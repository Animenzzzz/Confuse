# -*- coding: utf-8 -*-
import sys
import os
import randomvalue
import re
import json

file_type_pool = ["UIViewController","NSObject","UIView","UICollectionViewCell","UICollectionViewController","UITableViewCell","UITableViewController"]
file_name_pool = ["ViewController","Obj","View","CollectionViewCell","CollectionController","Cell","TableViewController"]

def create_h_m(outpath):

    index = randomvalue.intvalue(0,len(file_type_pool)-1)
    world = randomvalue.stringvalue()
    name = f'{world}{file_name_pool[index]}'

    newfile_h = open(f'{outpath}/{name}.h','w')
    h_string = f'#import <UIKit/UIKit.h>\nNS_ASSUME_NONNULL_BEGIN\n\n@interface {name} : {file_type_pool[index]}\n\n@end\n\nNS_ASSUME_NONNULL_END'
    newfile_h.write(h_string)
    newfile_h.close()

    newfile_m = open(f'{outpath}/{name}.m','w')
    m_string = f'#import \"{name}.h\"\n@implementation {name}\n\n@end'
    newfile_m.write(m_string)
    newfile_m.close()
    
