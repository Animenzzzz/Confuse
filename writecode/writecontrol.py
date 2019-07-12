# -*- coding: utf-8 -*-
import codemodel
import os

test_pat = "/Users/animenzzz/Desktop/aa.txt"

write_string = codemodel.if_model()
os.remove(test_pat)
file_te = open(test_pat, 'a+')
file_te.write(write_string)
file_te.close()
