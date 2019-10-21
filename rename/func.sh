#  Created by Animenzzz on 19/10/12.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.
#  此脚本，README有详细说明

#!/bin/bash

# 当前脚本工程的路径
FUNC_SH_PATH=$(cd `dirname $0`; pwd)
CONFUSE_PATH=${FUNC_SH_PATH%/*}

WORDS=`cat $CONFUSE_PATH/resource/words.txt`
IOS_WORDS=`cat $CONFUSE_PATH/resource/ioswords.txt`

WORDS_LIST=(${WORDS})
WORDS_LIST_COUNT=${#WORDS_LIST[@]}
IOS_WORDS_LIST=(${IOS_WORDS})
IOS_WORDS_LIST_COUNT=${#IOS_WORDS_LIST[@]}

# 此白名单下的文件、文件夹不做处理
IGNORE_FILE=("3rd" "core" "WebView")

echo "当前功能模块：【函数重命名】"
echo "1:特征函数混淆（如有特征前缀：qwe_） 2:所有.h的函数混淆  3: 1+2一起混淆"
read choosen_func
if [[ "${choosen_func}" = "1" || "${choosen_func}" = "3" ]];then
    echo "请输入特征前缀："
    read func_pre
fi

echo "请输入工程路径"
read projectPath

TABLENAME=symbols
SYMBOL_DB_FILE="/Users/animenzzz/Desktop/测试路径/symbols"
FUNC_LIST="/Users/animenzzz/Desktop/测试路径/func.list"
HEAD_FILE="${projectPath}/Obfuscation/Qwe_funcObfuscation.h"

function isIgnoreFile(){
    local fileName=${1}
    local result="NO"
    for ignore in ${IGNORE_FILE[@]};
    do
        if [[ "$fileName" = "$ignore" ]];then #是忽略的文件/文件夹
            result="YES"
            break
        fi
    done
    echo $result
}

rm -f $SYMBOL_DB_FILE
rm -f $FUNC_LIST
rm -f $HEAD_FILE

function getFuncList_pref(){
    #取以.m或.h结尾的文件以+号或-号开头的行 |去掉所有+号或－号|用空格代替符号|n个空格跟着<号 替换成 <号|开头不能是IBAction|用空格split字串取第二部分|排序|去重复|删除空行|删掉以init开头的行>写进func.list
    grep -h -r -I  "^[-+]" $1  --include '*.[mh]'\
    |sed "s/[+-]//g"\
    |sed "s/[();,: *\^\/\{]/ /g"\
    |sed "s/[ ]*</</"\
    |sed "/^[ ]*IBAction/d"\
    |sed "/^[ ]*instancetype/d"\
    |awk '{split($0,b," "); print b[2]; }'\
    |sort|uniq \
    |sed -n "/^${func_pre}/p" >>$FUNC_LIST
}

function getFuncList_allHM(){
    grep -h -r -I  "^[-+]" $1  --include '*.[mh]'\
    |sed "s/[+-]//g"\
    |sed "s/[();,: *\^\/\{]/ /g"\
    |sed "s/[ ]*</</"\
    |sed "/^[ ]*IBAction/d"\
    |sed "/^[ ]*instancetype/d"\
    |awk '{split($0,b," "); print b[2]; }'\
    |sort|uniq \
    |sed "/^set/d"\
    |sed "/^get/d"\
    |sed "/^init/d"\
    |sed "/^awakeFromNib/d"\
    |sed "/^viewDid/d"\
    |sed "/^viewWill/d"\
    |sed "/load/d"\
    |sed "/^sdk_/d"\
    |sed "/error/d"\
    |sed "/sharedInstance/d"\
    |sed "/^show/d"\
    |sed "/addButtonWithTitle/d"\
    |sed "/textFieldAtIndex/d"\
    |sed "/^dealloc/d" >>$FUNC_LIST
}

export LC_CTYPE=C

function travelFile(){

    ls "${1}" | while read f;
    do
        path=""${1}"/"${f}""

        ignoreFile=$(isIgnoreFile "$(basename $path)")

        if [ -d "${path}" ];then
            if [ "${ignoreFile}" = "NO" ];then
                travelFile "${path}"
            fi
        else
            if [ "${path##*.}" = "h" ];then
                if [ "${ignoreFile}" = "NO" ];then
                    getFuncList_allHM $path
                fi
            fi
        fi
    done
}

if [ "${choosen_func}" = "1" ];then #特征前缀
    getFuncList_pref $projectPath
elif [ "${choosen_func}" = "2" ];then #所有函数
    travelFile ${projectPath}
elif [ "${choosen_func}" = "3" ];then #所有函数
    if [ -n "$func_pre" ];then
        getFuncList_pref $projectPath
    fi
    travelFile ${projectPath}
fi

# ————————————————
# 版权声明：本文为CSDN博主「念茜」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/yiyaaixuexi/article/details/29201699
createTable()
{
    echo "create table $TABLENAME(src text, des text);" | sqlite3 $SYMBOL_DB_FILE
}

insertValue()
{
    echo "insert into $TABLENAME values('$1' ,'$2');" | sqlite3 $SYMBOL_DB_FILE
}

query()
{
    echo "select * from $TABLENAME where src='$1';" | sqlite3 $SYMBOL_DB_FILE
}

ramdomString()
{
    # openssl rand -base64 64 | tr -cd 'a-zA-Z' |head -c 16
    random_words=${WORDS_LIST[$((RANDOM%WORDS_LIST_COUNT))]}
    random_ios_words=${IOS_WORDS_LIST[$((RANDOM%IOS_WORDS_LIST_COUNT))]}
    echo ${random_words}${random_ios_words}
   
}

createTable

touch $HEAD_FILE
echo '#ifndef Demo_codeObfuscation_h
#define Demo_codeObfuscation_h' >> $HEAD_FILE
echo "//confuse string at `date`" >> $HEAD_FILE
cat "$FUNC_LIST" |sort|uniq | while read -ra line; do
    if [[ ! -z "$line" ]]; then
        ramdom=`ramdomString`
        echo $line $ramdom
        insertValue $line $ramdom
        echo "#define $line $ramdom" >> $HEAD_FILE
    fi
done
echo "#endif" >> $HEAD_FILE

sqlite3 $FUNC_LIST .dump



