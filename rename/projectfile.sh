#  Created by Animenzzz on 19/10/11.
#  Copyright (c) 2019年 Animenzzz. All rights reserved.

#!/bin/bash

# 此脚本，README有详细说明

echo "---项目将进行前缀重命名。"
echo "---当前项目的前缀："
read prefixOldName
echo "---请输入新前缀："
read prefixNewName
echo "---请输入当前工程项目的路径（项目整个文件夹）："
read oldFilePath
echo "---请输入结果输出的路径（新工程路径）："
read renameFilePath

# 旧工程的文件名
oldProjectName=$(basename $oldFilePath)
# 新工程的文件名
# ${string/#substring/replacement}   如果$string的前缀匹配$substring, 那么就用$replacement来代替匹配到的$substring
newProjectName=${oldProjectName/#$prefixOldName/$prefixNewName}

cp -r $oldFilePath $renameFilePath

newProjectPath="$renameFilePath/$newProjectName"
echo "---正在新建目录：$newProjectPath"

if [ "$renameFilePath/$oldProjectName" != "$newProjectPath" ];then
mv "$renameFilePath/$oldProjectName" "$newProjectPath"
fi

echo "---正在进行项目重命名..."
function travelFile(){

    ls "${1}" | while read f;
    do
        path=""${1}"/"${f}""
        destPath=${path//${prefixOldName}/${prefixNewName}}
        
        if [ -d "${path}" ];then
            if [ "$path" != "$destPath" ];then
                mv "${path}" "${destPath}"
            fi
            # mv "${path}" "${destPath}"
            travelFile "${destPath}"
        else
            if [ "$path" != "$destPath" ];then
                mv "${path}" "${destPath}"
            fi
            sed -i "s/${prefixOldName}/${prefixNewName}/g" "${destPath}"
        fi
    done
}
travelFile ${newProjectPath}