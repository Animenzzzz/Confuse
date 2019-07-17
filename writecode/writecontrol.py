# -*- coding: utf-8 -*-
import codemodel
import os
import linecache
import randomvalue
import filemanager

test_pat1 = "/Users/animenzzz/Desktop"
test_pat = "/Users/animenzzz/Desktop/aa.txt"
random_func_path = "/Users/animenzzz/GitCode/Confuse/resource/random_func_create.txt"

work_path = "/Users/animenzzz/GitCode/Confuse/resource"
file_json_path1 = f"{work_path}/func_analysised/uikit_class_func.txt"


func_dic = randomvalue.funccreate(random_func_path,3)

filemanager.create_h_m(test_pat1)



# func_arr = []
# funcfile = open(file_json_path1,'r')
# lengh = len(funcfile.readlines())
# funcfile.close()
# for i in range(1,3):
#     random_row = randomvalue.intvalue(1,lengh)
#     random_line = linecache.getline(file_json_path1, random_row)
#     func_arr.append(random_line)
# if os.path.exists(random_func_path):
#     os.remove(random_func_path)
# write_string = codemodel.func_model(1,1,1,func_arr,1,random_func_path)
# if write_string != "":
#     os.remove(test_pat)
#     file_te = open(test_pat, 'a+')
#     file_te.write(write_string)
#     file_te.close()

# funcfile = open(file_json_path1,'r')
# lengh = len(funcfile.readlines())
# funcfile.close()
# random_row = randomvalue.intvalue(1,lengh)
# random_line = linecache.getline(file_json_path1, random_row)
# write_string = codemodel.func_call_model(random_line,1)
# if write_string != "":
#     os.remove(test_pat)
#     file_te = open(test_pat, 'a+')
#     file_te.write(write_string)
#     file_te.close()


# write_string = codemodel.if_model()
# os.remove(test_pat)
# file_te = open(test_pat, 'a+')
# file_te.write(write_string)
# file_te.close()


# write_string = codemodel.switch_model()
# os.remove(test_pat)
# file_te = open(test_pat, 'a+')
# file_te.write(write_string)
# file_te.close()
