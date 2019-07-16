# -*- coding: utf-8 -*-
import sys
import os
import re
import json
def func(funcstring,jsonoutputfile):

    #获取参数类型，返回值类型
    matchObj = re.findall('\((.*?)\)', funcstring)
    resultDic = {}
    resultDic["params"] = {}

    if matchObj:
        resultDic["returntype"] = matchObj[0]
        for num in range(1,len(matchObj)): 
            resultDic["params"] = matchObj[1:len(matchObj)]
    
    #获取函数名，参数描述
    descrip = re.sub(u'\((.*?)\)', "",funcstring)
    list1 = descrip.split(' ')
    descriparr = []
    if descrip:
        index = str(list1[1]).find(":")
        funcname_string = str(list1[1])[0:index]
        resultDic["funcname"] = str(funcname_string).strip(";")
        for num in range(2,len(list1)):
            tmp = str(list1[num])
            index = tmp.find(":")
            tmp1 = tmp[0:index]
            descriparr.append(tmp[0:index])
        resultDic["descrip"] = descriparr
    
    jsonfile = open(jsonoutputfile,'a+')
    jsonfile.writelines(json.dumps(resultDic)+'\n')
    jsonfile.close()