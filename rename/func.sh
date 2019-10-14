#  Created by Animenzzz on 19/10/12.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.
#  此脚本，README有详细说明

#!/bin/bash

FUNC_LIST="/Users/animenzzz/Desktop/测试路径/func.txt"
rm -f $FUNC_LIST

echo "请输入工程路径"
# read projectPath
projectPath="/Users/animenzzz/GitCode/TTSDK/ttsdk-for-appstore/WSXGameSDKDemo/WSXGameSDK"

function getFuncList(){
    fileName=$(basename $1)
    #取以.m或.h结尾的文件以+号或-号开头的行 |去掉所有+号或－号|用空格代替符号|n个空格跟着<号 替换成 <号|开头不能是IBAction|用空格split字串取第二部分|排序|去重复|删除空行|删掉以init开头的行>写进func.list
    echo "类名：${fileName}" >> $FUNC_LIST
    grep -h -r -I  "^[-+]" $1  --include '*.[mh]'\
    |sed "s/[+-]//g"\
    |sed "s/[();,: *\^\/\{]/ /g"\
    |sed "s/[ ]*</</"\
    |sed "/^[ ]*IBAction/d"\
    |awk '{split($0,b," "); print b[2]; }'\
    |sort|uniq \
    |sed "/^set/d"\
    |sed "/^get/d"\
    |sed "/^init/d"\
    |sed "/^awakeFromNib/d"\
    |sed "/^viewDid/d"\
    |sed "/^viewWill/d"\
    |sed "/load/d"\
    |sed "/^dealloc/d" >>$FUNC_LIST
    # if [ ${#SPECIA_FUNC_PREFIX[@]} -eq 0 ]; then
    #     echo "为0"

    # else
    #     echo "不为0"
    # fi
}

export LC_CTYPE=C

function travelFile(){

    ls "${1}" | while read f;
    do
        path=""${1}"/"${f}""

        if [ -d "${path}" ];then
            travelFile "${path}"
        else
            if [ "${path##*.}" = "m" ];then
                getFuncList $path
            fi
        fi
    done
}

travelFile ${projectPath}
open $FUNC_LIST


