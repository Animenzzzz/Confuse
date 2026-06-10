#  Created by Animenzzz on 19/10/12.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.
#  此脚本，README有详细说明

#!/bin/bash

# 当前脚本工程的路径
FUNC_SH_PATH=$(cd "$(dirname "$0")" && pwd)
CONFUSE_PATH=${FUNC_SH_PATH%/*}

# shellcheck source=common.sh
source "$FUNC_SH_PATH/common.sh"
load_rename_profile "$@"

IGNORE_FILE=("${FUNC_IGNORE_FILE[@]}")

WORDS_FILE="$CONFUSE_PATH/resource/words.txt"
IOS_WORDS_FILE="$CONFUSE_PATH/resource/ioswords.txt"
if [[ ! -f "$WORDS_FILE" || ! -f "$IOS_WORDS_FILE" ]]; then
    echo "词库缺失，请在 resource/ 下准备 words.txt 与 ioswords.txt（见 README）" >&2
    exit 1
fi

WORDS=$(cat "$WORDS_FILE")
IOS_WORDS=$(cat "$IOS_WORDS_FILE")

WORDS_LIST=(${WORDS})
WORDS_LIST_COUNT=${#WORDS_LIST[@]}
IOS_WORDS_LIST=(${IOS_WORDS})
IOS_WORDS_LIST_COUNT=${#IOS_WORDS_LIST[@]}

echo "当前功能模块：【函数重命名】"
echo "当前 profile：$CONFUSE_PROFILE"
echo "1:特征函数混淆（如有特征前缀：qwe_） 2:所有.h的函数混淆  3: 1+2一起混淆"
read -r choosen_func
if [[ "${choosen_func}" = "1" || "${choosen_func}" = "3" ]]; then
    echo "请输入特征前缀："
    read -r func_pre
fi

echo "请输入工程路径"
read -r projectPath

TABLENAME=symbols
WORK_DIR="$CONFUSE_PATH/$FUNC_WORK_SUBDIR"
mkdir -p "$WORK_DIR"
mkdir -p "${projectPath}/${OBFUSCATION_SUBDIR}"
SYMBOL_DB_FILE="$WORK_DIR/symbols"
FUNC_LIST="$WORK_DIR/func.list"
HEAD_FILE="${projectPath}/${OBFUSCATION_SUBDIR}/${OBFUSCATION_HEADER}"

function isIgnoreFile(){
    local fileName=${1}
    local result="NO"
    for ignore in "${IGNORE_FILE[@]}";
    do
        if [[ "$fileName" = "$ignore" ]]; then
            result="YES"
            break
        fi
    done
    echo "$result"
}

rm -f "$SYMBOL_DB_FILE"
rm -f "$FUNC_LIST"
rm -f "$HEAD_FILE"

function getFuncList_pref(){
    grep -h -r -I  "^[-+]" "$1"  --include '*.[mh]'\
    |sed "s/[+-]//g"\
    |sed "s/[();,: *\^\/\{]/ /g"\
    |sed "s/[ ]*</</"\
    |sed "/^[ ]*IBAction/d"\
    |sed "/^[ ]*instancetype/d"\
    |awk '{split($0,b," "); print b[2]; }'\
    |sort|uniq \
    |sed -n "/^${func_pre}/p" >>"$FUNC_LIST"
}

function getFuncList_allHM(){
    grep -h -r -I  "^[-+]" "$1"  --include '*.[mh]'\
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
    |sed "/^dealloc/d" >>"$FUNC_LIST"
}

export LC_CTYPE=C

function travelFile(){

    ls "${1}" | while read -r f;
    do
        path="${1}/${f}"

        ignoreFile=$(isIgnoreFile "$(basename "$path")")

        if [ -d "${path}" ]; then
            if [ "${ignoreFile}" = "NO" ]; then
                travelFile "${path}"
            fi
        else
            if [ "${path##*.}" = "h" ]; then
                if [ "${ignoreFile}" = "NO" ]; then
                    getFuncList_allHM "$path"
                fi
            fi
        fi
    done
}

if [ "${choosen_func}" = "1" ]; then
    getFuncList_pref "$projectPath"
elif [ "${choosen_func}" = "2" ]; then
    travelFile "${projectPath}"
elif [ "${choosen_func}" = "3" ]; then
    if [ -n "$func_pre" ]; then
        getFuncList_pref "$projectPath"
    fi
    travelFile "${projectPath}"
fi

createTable()
{
    echo "create table $TABLENAME(src text, des text);" | sqlite3 "$SYMBOL_DB_FILE"
}

insertValue()
{
    echo "insert into $TABLENAME values('$1' ,'$2');" | sqlite3 "$SYMBOL_DB_FILE"
}

query()
{
    echo "select * from $TABLENAME where src='$1';" | sqlite3 "$SYMBOL_DB_FILE"
}

ramdomString()
{
    random_words=${WORDS_LIST[$((RANDOM%WORDS_LIST_COUNT))]}
    random_ios_words=${IOS_WORDS_LIST[$((RANDOM%IOS_WORDS_LIST_COUNT))]}
    echo "${random_words}${random_ios_words}"
}

createTable

touch "$HEAD_FILE"
echo "#ifndef ${OBFUSCATION_HEADER_GUARD}
#define ${OBFUSCATION_HEADER_GUARD}" >> "$HEAD_FILE"
echo "//confuse string at $(date)" >> "$HEAD_FILE"
cat "$FUNC_LIST" |sort|uniq | while read -ra line; do
    if [[ ! -z "$line" ]]; then
        ramdom=$(ramdomString)
        echo "$line" "$ramdom"
        insertValue "$line" "$ramdom"
        echo "#define $line $ramdom" >> "$HEAD_FILE"
    fi
done
echo "#endif" >> "$HEAD_FILE"

sqlite3 "$FUNC_LIST" .dump
