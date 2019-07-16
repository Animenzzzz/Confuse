# -*- coding: utf-8 -*-
import codemodel
import os
import linecache
import randomvalue
test_pat = "/Users/animenzzz/Desktop/aa.txt"


work_path = "/Users/animenzzz/GitCode/Confuse/resource"
file_json_path1 = f"{work_path}/func_analysised/uikit_class_func.txt"



funcfile = open(file_json_path1,'r')
lengh = len(funcfile.readlines())
funcfile.close()
random_row = randomvalue.intvalue(1,lengh)
random_line = linecache.getline(file_json_path1, random_row)
write_string = codemodel.func_model(random_line,1)
if write_string != "":
    os.remove(test_pat)
    file_te = open(test_pat, 'a+')
    file_te.write(write_string)
    file_te.close()


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
