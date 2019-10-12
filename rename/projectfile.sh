#  Created by Animenzzz on 19/10/11.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.
#  此脚本，README有详细说明

#!/bin/bash

# 此白名单下的文件、文件夹不做处理
IGNORE_FILE=("Build" \
"Index" \
".gitignore" \
".vscode" \
".git" \
"README.md" \
)

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

echo "当前功能模块：【前缀重命名】"
echo "请输入当前项目的前缀："
read prefixOldName
echo "请输入新前缀："
read prefixNewName
echo "请输入当前工程项目的路径（项目整个文件夹）："
read oldFilePath
echo "请输入输出的路径（新工程路径）："
read renameFilePath

# 旧工程的文件名
oldProjectName=$(basename $oldFilePath)
# 新工程的文件名
# ${string/#substring/replacement}   如果$string的前缀匹配$substring, 那么就用$replacement来代替匹配到的$substring
newProjectName=${oldProjectName/#$prefixOldName/$prefixNewName}

newProjectPath="$renameFilePath/$newProjectName"
echo "正在新建目录：$newProjectPath"
mkdir $newProjectPath
if [ "$renameFilePath/$oldProjectName" != "$newProjectPath" ];then
mv "$renameFilePath/$oldProjectName" "$newProjectPath"
fi

echo "正在进行项目重命名..."
function travelFile(){

    ls "${1}" | while read f;
    do
        old_path=""${1}"/"${f}""
        new_path=""${2}"/"${f}""
        destPath=${new_path//${prefixOldName}/${prefixNewName}}

        ignoreFile=$(isIgnoreFile "$(basename $old_path)")

        if [ -d "${old_path}" ];then
            if [ "${ignoreFile}" = "NO" ];then 
                mkdir "${destPath}"
                travelFile "${old_path}" "${destPath}"
            fi
        else
            if [ "${ignoreFile}" = "NO" ];then
                cp "${old_path}" "${destPath}"
                sed -i "s/${prefixOldName}/${prefixNewName}/g" "${destPath}"
            fi
        fi
    done
}
travelFile ${oldFilePath} ${newProjectPath}
open $newProjectPath