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

# How to use
#### 1.```config.py```中，白名单文件夹的设置（只在此白名单中的文件才进行垃圾代码的写入）
#### 2.```config.py```中，对```call_all_class```进行设置
	1)若设置为空，则默认创建  工程名+AllCall  类作为控制开关
	2)若设置为  XXXX  ，则需要在指定工程文件  .xcodeproj  的同级目录创建  HX  文件夹，且在此文件夹新建 XXXX.h，XXXX.m 两个文件
  
#### 3.脚本说明
	假设工程的  .xcodeproj 路径为：/Users/animenzzz/XPlatformKit/XPlatformKit.xcodeproj
	1.根据假设，则HX目录为 /Users/animenzzz/XPlatformKit/HX
	2.根据假设，则白名单某个文件夹的路径为：/Users/animenzzz/XPlatformKit/XPlatformKit/白名单文件夹
	3.输入的文件路径为 .xcodeproj 的上一级目录
	如：根据假设：则为/Users/animenzzz/XPlatformKit
