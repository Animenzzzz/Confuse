#  Created by Animenzzz on 19/10/11.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.
#  此脚本，README有详细说明

#!/bin/bash

PROJECTFILE_SH_PATH=$(cd "$(dirname "$0")" && pwd)
CONFUSE_PATH=${PROJECTFILE_SH_PATH%/*}

# shellcheck source=common.sh
source "$PROJECTFILE_SH_PATH/common.sh"
load_rename_profile "$@"

IGNORE_FILE=("${PROJECT_IGNORE_FILE[@]}")

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

echo "当前功能模块：【前缀重命名】"
echo "当前 profile：$CONFUSE_PROFILE"
echo "请输入当前项目的前缀："
read -r prefixOldName
echo "请输入新前缀："
read -r prefixNewName
echo "请输入当前工程项目的路径（项目整个文件夹）："
read -r oldFilePath
echo "请输入输出的路径（新工程路径）："
read -r renameFilePath

oldProjectName=$(basename "$oldFilePath")
newProjectName=${oldProjectName/#$prefixOldName/$prefixNewName}

newProjectPath="$renameFilePath/$newProjectName"
echo "正在新建目录：$newProjectPath"
mkdir -p "$newProjectPath"

echo "正在进行项目重命名..."
function travelFile(){

    ls "${1}" | while read -r f;
    do
        old_path="${1}/${f}"
        new_path="${2}/${f}"
        destPath=${new_path//${prefixOldName}/${prefixNewName}}

        ignoreFile=$(isIgnoreFile "$(basename "$old_path")")

        if [ -d "${old_path}" ]; then
            if [ "${ignoreFile}" = "NO" ]; then
                mkdir -p "${destPath}"
                travelFile "${old_path}" "${destPath}"
            fi
        else
            if [ "${ignoreFile}" = "NO" ]; then
                cp "${old_path}" "${destPath}"
                sed -i '' "s/${prefixOldName}/${prefixNewName}/g" "${destPath}"
            fi
        fi
    done
}
travelFile "${oldFilePath}" "${newProjectPath}"
open "$newProjectPath"
