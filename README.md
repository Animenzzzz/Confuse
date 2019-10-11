# Confuse
此脚本用于iOS工程（Objective-C）的混淆，包括垃圾代码的写入、项目重命名

```
Confuse
├── README.md                                      // help
├── resource                                       // 资源
│   ├── random_func_create.txt
│   ├── random_class_name.txt                      //
│   ├── ioswords.txt                               // iOS风格词库
│   ├── words.txt                                  // 普通词库
│   ├── func_orign                                 // 
│       ├── uikit_member_instancetype_func.txt
│       ├── uikit_member_instancetype_func.txt
│       ├── uikit_member_instancetype_func.txt
│       └── uikit_member_instancetype_func.txt
│   └── func_orign                                 // 
│       ├── uikit_member_instancetype_func.txt
│       ├── uikit_member_instancetype_func.txt
│       ├── uikit_member_instancetype_func.txt
│       └── uikit_member_instancetype_func.txt
├── writecode
├── doc                                            // 文档
├── static                                         // web静态资源加载
│   └── initjson
│       └── config.js                              // 提供给前端的配置
├── test
├── test-service.js
└── tools
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
  

