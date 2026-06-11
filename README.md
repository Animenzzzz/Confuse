# Confuse

iOS 工程（Objective-C）混淆工具集：垃圾代码注入、工程前缀重命名、函数宏混淆。

## 目录结构

```
Confuse/
├── README.md
├── profiles/                          # 工程相关配置（按 profile 隔离，便于移植）
│   └── default/                       # 示例 profile，可复制为新工程
│       ├── writecode.json             # 垃圾代码写入：白名单、数量、开关类名等
│       └── rename.env                 # 重命名：白名单、临时目录、宏头文件路径等
├── resource/                          # 共享资源（词库、UIKit API 解析结果等）
│   ├── words.txt                      # 通用英文词库（内置，一行一词）
│   ├── ioswords.txt                   # iOS/OC 风格后缀词库（内置）
│   ├── random_func_create.txt         # 运行时生成，Git 忽略
│   ├── random_class_name.txt          # 运行时生成，Git 忽略
│   ├── func_orign/                    # iOS 原生 API 原文
│   └── func_analysised/               # 经 analysis 解析后的 API 字典
├── writecode/                         # 垃圾代码写入模块
│   ├── config.py                      # 加载 profile + 运行时路径
│   ├── profile_loader.py              # profile 解析与 JSON 读取
│   ├── writecontrol.py                # 入口脚本
│   ├── codemodel.py / filemanager.py / randomvalue.py
│   ├── xcodeprojhelp.rb
│   └── analysis/                      # 原生 SDK 解析（analys.py）
├── rename/                            # 重命名模块
│   ├── common.sh                      # 加载 profile 的公共逻辑
│   ├── projectfile.sh                 # 工程前缀重命名
│   └── func.sh                        # 函数宏混淆
└── .work/                             # func.sh 临时 sqlite/列表（Git 忽略）
```

## Profile：创建与切换

工具核心（`writecode/`、`rename/`、`resource/`）与**工程配置**分离。每个 iOS 工程建议复制一份 profile：

```bash
cp -R profiles/default profiles/my_app
# 编辑 profiles/my_app/writecode.json
# 编辑 profiles/my_app/rename.env
```

切换 profile 的两种方式（二选一）：

```bash
# 环境变量
export CONFUSE_PROFILE=my_app

# 或命令行参数
python3 writecode/writecontrol.py --profile my_app
sh rename/func.sh --profile my_app
sh rename/projectfile.sh --profile my_app
```

未指定时默认使用 `default`。

### writecode.json 字段说明

| 字段 | 说明 |
|------|------|
| `file_while_list` | 白名单文件夹名（仅这些目录下的 `.h/.m` 可写入垃圾代码） |
| `m_h_num_min` / `m_h_num_max` | 每个文件生成属性/方法数量的范围 |
| `call_all_class` | 控制开关类名；空字符串则自动创建「工程名+AllCall」 |
| `call_func_name` | 开关类中的入口方法名 |
| `hx_folder` | 使用自定义开关类时，`.h/.m` 所在子目录名（默认 `HX`） |

### rename.env 字段说明

| 变量 | 说明 |
|------|------|
| `FUNC_IGNORE_FILE` | func.sh 遍历工程时跳过的文件夹 |
| `PROJECT_IGNORE_FILE` | projectfile.sh 复制时跳过的文件/文件夹 |
| `FUNC_WORK_SUBDIR` | 符号表、func.list 等临时文件目录（相对仓库根） |
| `OBFUSCATION_SUBDIR` | 宏头文件相对工程路径的子目录 |
| `OBFUSCATION_HEADER` | 生成的宏头文件名 |
| `OBFUSCATION_HEADER_GUARD` | 头文件 `#ifndef` 宏名 |

## 环境

- macOS
- Python 3
- Ruby（writecontrol 修改 `.xcodeproj` 时需要）
- sqlite3（func.sh）

## 词库说明

`rename/func.sh` 与 `writecode/randomvalue.py` 依赖 `resource/words.txt` 与 `resource/ioswords.txt` 生成随机符号名。**仓库已内置**两份词库（各约 1000 词），路径固定为 `resource/`，与 profile 无关。

| 文件 | 用途 | 格式 |
|------|------|------|
| `words.txt` | 通用英文单词（变量名、参数标签、类名片段等） | **一行一词**的合法 OC 标识符（字母开头，仅字母数字）；空行与 `#` 开头注释行会被忽略 |
| `ioswords.txt` | iOS/OC 风格后缀（如 `View`、`Controller`、`Manager`） | 同上；与 `words.txt` 随机组合成函数名（如 `fetchData` + `Handler`） |

扩展词库：编辑上述文件后追加单词（每行一个词）。可用 `resource/_generate_wordlists.py` 重新生成或作参考。建议避免与 UIKit/Foundation 类名、保留字（`init`、`dealloc` 等）完全相同的单词。

## 使用流程

### 一、垃圾代码写入（writecontrol.py）

**命令：**

```bash
python3 /path/to/Confuse/writecode/writecontrol.py
# 或指定 profile
python3 /path/to/Confuse/writecode/writecontrol.py --profile default
```

**交互说明：**

假设工程 `.xcodeproj` 为 `/Users/you/MyApp/MyApp.xcodeproj`：

1. `HX` 目录（或使用自定义开关类时）为 `/Users/you/MyApp/HX`
2. 白名单文件夹路径示例：`/Users/you/MyApp/MyApp/Services`
3. 输入的路径为 `.xcodeproj` 的**上一级目录**：`/Users/you/MyApp`

**配置（在 profile 中修改，而非改代码）：**

1. `writecode.json` 的 `file_while_list`：仅白名单内文件夹参与写入
2. `call_all_class`：
   - 留空：自动创建「工程名+AllCall」类
   - 设为 `XSDKAllCall` 等：需在工程同级 `HX`（或 `hx_folder`）下已有对应 `.h/.m`

### 二、工程前缀重命名（projectfile.sh）

**命令：**

```bash
sh /path/to/Confuse/rename/projectfile.sh
```

脚本会**拷贝**旧工程到新目录并在副本上重命名，不影响原工程。白名单在 profile 的 `PROJECT_IGNORE_FILE` 中配置。

### 三、函数宏混淆（func.sh）

**命令：**

```bash
sh /path/to/Confuse/rename/func.sh
```

1. 在 profile 的 `FUNC_IGNORE_FILE` 中配置不需处理的目录
2. 三种模式：特征前缀混淆 / 全部 `.h` 声明 / 两者兼有
3. 生成的宏头文件路径由 `OBFUSCATION_*` 配置；临时数据库在 `.work/<profile>/`

跑完后请手动检查宏头文件，删除误混淆的系统方法声明。

### 四、（可选）重新生成 UIKit API 解析文件

```bash
python3 /path/to/Confuse/writecode/analysis/analys.py
```

路径已相对仓库根目录，无需改本机绝对路径。

## 典型移植步骤

1. 复制 `profiles/default` 为新 profile 名
2. 按目标工程修改 `writecode.json` 与 `rename.env`
3. （可选）按需扩展 `resource/words.txt`、`resource/ioswords.txt`
4. 使用 `CONFUSE_PROFILE=新名` 或 `--profile 新名` 运行各脚本
