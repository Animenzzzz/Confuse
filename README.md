# Confuse
此脚本用于iOS工程（Objective-C）的混淆，包括垃圾代码的写入、项目重命名

```
Confuse
├── README.md                                      // help
├── resource                                       // 脚本所需的资源库
│   ├── random_func_create.txt                     // 脚本一次运行创建的随机方法名(Git上忽略其修改)
│   ├── random_class_name.txt                      // 脚本一次运行创建的随机类名(Git上忽略其修改)
│   ├── ioswords.txt                               // iOS风格词库
│   ├── words.txt                                  // 普通词库
│   ├── func_orign                                 // 此文件夹下是iOS的原生API
│   │   ├── uikit_member_instancetype_func.txt
│   │   ├── uikit_member_func.txt
│   │   ├── uikit_class_instancetype_func.txt
│   │   └── uikit_class_func.txt
│   └── func_analysised                            // 此文件夹下是原生API经过脚本(analysis)解析成字典的格式，为了便于使用
│       ├── uikit_member_instancetype_func.txt
│       ├── uikit_member_func.txt
│       ├── uikit_class_instancetype_func.txt
│       └── uikit_class_func.txt
├── writecode                                      // 垃圾代码写入模块
│   ├── config.py                                  // 脚本配置（需要根据工程进行修改配置，见下文）
│   ├── xcodeprojhelp.rb                           // .xcoproject操作脚本（用于给创建的垃圾代码文件添加、修改引用等）
│   ├── codemodel.py                               // 垃圾代码样式模块（包括分支语句、函数调用语句、循环语句等）
│   ├── filemanager.py                             // 文件操作模块（新建文件、对文件进行读写等）
│   ├── writecontrol.py                            // 脚本入口
│   ├── randomvalue.py                             // 产生随机值（函数名、类名等）
│   └── analysis                                   // 原生SDK解析脚本
│       ├── analysisstring.py
│       └── analys.py
└── rename                                         // 前缀重命名模块
    └── projectfile.sh                             // 脚本入口
```

# 环境
安装好python3，脚本环境：MacOS

# 使用
### 一、垃圾代码写入(writecontrol.py)
#### （1）命令：
	python3 yourpath/Confuse/writecode/writecontrol.py
#### （2）脚本说明：
	假设工程的  .xcodeproj 路径为：/Users/animenzzz/XPlatformKit/XPlatformKit.xcodeproj
	1.则HX目录为 /Users/animenzzz/XPlatformKit/HX
	2.则白名单某个文件夹的路径为：/Users/animenzzz/XPlatformKit/XPlatformKit/白名单文件夹
	3.输入的文件路径为 .xcodeproj 的上一级目录，如：/Users/animenzzz/XPlatformKit
#### （3）根据你的工程修改：
	1. config.py 中，白名单文件夹的设置（只在此白名单中的文件才进行垃圾代码的写入）
	2. config.py 中，对 call_all_class 进行设置
	 1)若设置为空，则默认创建 工程名+AllCall 类作为控制开关
	 2)若设置为 XXXX ，则需要在指定工程文件 .xcodeproj 的同级目录创建 HX 文件夹，且在此文件夹新建 XXXX.h，XXXX.m 两个文件

### 二、项目前缀重命名(projectfile.py)
#### （1）命令：
	python3 yourpath/Confuse/rename/projectfile.sh
#### （2）脚本说明：
	1.此脚本会拷贝你的旧工程，并在这个备份进行重命名，不会对原工程有影响
	
#### （3）根据你的工程修改：
	1. 在白名单中添加你不需要更改的内容。。TODO。。。
  

